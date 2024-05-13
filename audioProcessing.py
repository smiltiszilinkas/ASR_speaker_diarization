from pydub import AudioSegment
from pydub.effects import normalize
import os
import random
import json
from timeConversion import seconds_to_miliseconds, time_to_miliseconds
from videoAudioData import video_data
import numpy as np



def get_audio_files_count():

  # Initialize count
  wav_file_count = 0

  # Iterate over files in the directory
  for filename in os.listdir('data/audioClips/'):
      # Check if the file is a .wav file
      if filename.endswith(".wav"):
          # Increment count
          wav_file_count += 1

  return wav_file_count

# Function to combine random audio clips
def combine_random_audio_clips(iterations):
  generated_combinations = set()  # Keep track of generated combinations
  # for iteration in range(iterations):
  while len(generated_combinations) != iterations:
    number_of_clips = random.randint(1,10)
    combined_audio = AudioSegment.empty()
    audio_meta = []
    for clip in range(number_of_clips):
      random_audio_clip = random.randint(0,get_audio_files_count()-1)
      audio_meta.append(random_audio_clip)
      audio = AudioSegment.from_wav(f'data/audioClips/{random_audio_clip}.wav')
      combined_audio += audio
    # Convert audio_meta to tuple for membership check
    audio_meta_tuple = tuple(audio_meta)
    # Check if it already exists
    if audio_meta_tuple not in generated_combinations and combined_audio.duration_seconds < 101:
      # Normalize the combined audio
      combined_audio = normalize(combined_audio)
      # Write normalized file
      combined_audio.export(f"data/combinedAudioClips/combined_audio_{len(generated_combinations)}.wav", format="wav")
      # Export audio meta to a JSON file
      with open(f"data/combinedAudioClips/audio_meta_{len(generated_combinations)}.json", "w") as file:
        json.dump(audio_meta, file)
      #Add to combinations
      generated_combinations.add(audio_meta_tuple)

# Function to read audio meta from JSON file
def read_audio_meta_from_json(file_path):
  with open(file_path, "r") as file:
      audio_meta = json.load(file)
  return audio_meta

# Function to find matching audio files based on the clip number
def find_matching_audio_files(audio_meta):
  matching_audio_files = []
  for audio_clip in audio_meta:
      matching_audio_files.append(video_data[audio_clip])
  return matching_audio_files

# Function to get all the speakers and their intervals from audio file
def get_intervals_from_audio(audio_meta):
  found_files = find_matching_audio_files(audio_meta)
  speakers = []
  speaker_count = 0
  start = time_to_miliseconds("00:00:000")

  for file in found_files:
    duration = seconds_to_miliseconds(file[7])
    end_time = start + duration 
    #checks if there is already speaker defined if yes appends the interval otherwise creates a new speaker
    if speaker_count != 0:
      speaker_exist = False
      for speaker in speakers:
        if speaker['name'] == file[1]:
          speaker_exist = True
          interval_object = {'start':start, 'end': end_time}
          speaker['intervals'].append(interval_object)
          
      if not speaker_exist:
          interval_object = {'start':start, 'end': end_time}
          speaker = {'name': file[1], 'intervals': [interval_object]}
          speakers.append(speaker)
    else:
      speaker_count += 1
      interval_object = {'start':start, 'end': end_time}
      speaker = {'name':file[1], 'intervals':[interval_object]}
      speakers.append(speaker)  
    start = end_time

  return speakers


def calculate_accuracy(correct_labels, predicted_labels):
  total_correct = 0
  total_predicted = len(predicted_labels)

  for pred_label in predicted_labels:
      pred_start, pred_end, pred_speaker = parse_predicted_label(pred_label)
      if pred_speaker < total_predicted:
        for interval in correct_labels[pred_speaker]['intervals']:
            if pred_start >= interval['start'] and pred_end <= interval['end']:
                total_correct += 1
                break

  accuracy = total_correct / total_predicted if total_predicted != 0 else 0
  return accuracy

def parse_predicted_label(predicted_label):
  parts = predicted_label.split()
  start_time = int(parts[0].split('=')[1].replace('ms', ''))
  end_time = int(parts[1].split('=')[1].replace('ms', ''))
  speaker = int(parts[2].split('SPEAKER_')[1])
  return start_time, end_time, speaker

def reorder_labels(predicted_labels):
  speaker_map = {}
  new_predicted_labels = []

  for label in predicted_labels:
      parts = label.split()
      speaker = parts[2]
      if speaker not in speaker_map:
          speaker_map[speaker] = f"SPEAKER_{len(speaker_map):02d}"
      new_label = f"{parts[0]} {parts[1]} {speaker_map[speaker]}"
      new_predicted_labels.append(new_label)

  return new_predicted_labels

def add_noise_to_combined_files(noise_level, clips_number):
  for clip in range(clips_number):
    # Load the audio file using PyDub
    audio = AudioSegment.from_file(f'data/combinedAudioClips/combined_audio_{clip}.wav')

    # Convert audio to raw PCM data
    audio_raw = audio.raw_data
    
    # Convert raw PCM data to numpy array
    audio_array = np.frombuffer(audio_raw, dtype=np.int16)
    
    # Generate noise
    noise = np.random.normal(0, 1, len(audio_array))
    
    # Calculate the scaling factor based on the desired noise level
    max_amplitude = np.max(np.abs(audio_array))
    scale_factor = noise_level * max_amplitude / np.max(np.abs(noise))
    
    # Scale the noise based on the calculated scaling factor
    noise *= scale_factor
    
    # Add noise to the audio data
    noisy_audio_array = audio_array + noise
    
    # Clip the noisy audio data to ensure it stays within the appropriate range [-32768, 32767]
    noisy_audio_array = np.clip(noisy_audio_array, -32768, 32767)
    
    # Convert the noisy audio array back to bytes
    noisy_audio_raw = noisy_audio_array.astype(np.int16).tobytes()
    
    # Create a new AudioSegment from the noisy audio raw data
    if audio.channels == 1:
        # If the original audio is mono, set the new audio to mono
        noisy_audio = AudioSegment(noisy_audio_raw, frame_rate=audio.frame_rate, sample_width=audio.sample_width, channels=1)
    else:
        # If the original audio is stereo, set the new audio to stereo
        noisy_audio = AudioSegment(noisy_audio_raw, frame_rate=audio.frame_rate, sample_width=audio.sample_width, channels=2)
    
    # Save the noisy audio to a new .wav file
    noisy_audio.export(f'data/combinedAudioClips/combined_audio_noise_{str(noise_level)}_{clip}.wav', format="wav")
