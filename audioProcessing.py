from pydub import AudioSegment
from pydub.effects import normalize
import os
import random
import json
from videoAudioData import video_data



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
  for iteration in range(iterations):
    number_of_clips = random.randint(2,10)
    combined_audio = AudioSegment.empty()
    audio_meta = []
    for clip in range(number_of_clips):
      random_audio_clip = random.randint(0,get_audio_files_count()-1)
      audio_meta.append(random_audio_clip)
      audio = AudioSegment.from_wav(f'data/audioClips/{random_audio_clip}.wav')
      combined_audio += audio

    # Normalize the combined audio
    combined_audio = normalize(combined_audio)
    # Write normalized file
    combined_audio.export(f"data/combinedAudioClips/combined_audio_{iteration}.wav", format="wav")
    # Export audio meta to a JSON file
    with open(f"data/combinedAudioClips/audio_meta_{iteration}.json", "w") as file:
      json.dump(audio_meta, file)

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
