# ASR_speaker_diarization

## Virtual environment python

1. Have VS code and Python installed
2. Create virtual environment as it is easy to manage all the libraries. Command: python -m venv venv
3. Activate virtual environment. Command: .\venv\Scripts\activate
4. Install all the required libraries: Command: pip install -r requirements.txt
5. Run any file on virtual environment. Command: python [name]
6. To quit virtual environment. Command: deactivate

## Ubuntu venv

1. cd venv
2. source bin/activate

## Ubuntu git ponyland

1. git clone https://smiltiszilinkas@github.com/smiltiszilinkas/ASR_speaker_diarization.git
2. git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
3. Personal Access Token (PAT):

Generate a personal access token on GitHub. You can do this by going to your GitHub account settings, then selecting "Developer settings" > "Personal access tokens" > "Generate new token".
Make sure to grant the necessary permissions for the token, such as repo access.
Once generated, use the generated token as your password when prompted for authentication during the git push operation.

4. git add .
5. git commit -m "your message"
6. git push origin <branch>
