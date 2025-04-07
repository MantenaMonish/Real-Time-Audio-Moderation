# Real-Time-Audio-Moderation
Real-Time Audio Moderation: A Privacy-Preserving Solution for Detecting Inappropriate Content

# Profanity Tagger
Audio processing system that transcribes and tags audio files for profanity.

## Features
- Automatic speech-to-text transcription using Whisper
- Profanity detection using better-profanity
- Web interface for file upload and results viewing
- Ngrok integration for public URL

## Installation
 ```bash
git clone https://github.com/yourusername/profanity-tagger.git
cd profanity-tagger
pip install -r requirements.txt
 ```

## After Installation
- Remove the .txt file in the data/WatchAudio/
- Check if all the files installed are in this order
 ```bash
📁 AudioMod-OS version/
│
├── tagger.py             # Handles audio transcription + profanity tagging
├── ui_windows.py         # Windows-specific GUI and watch folder
├── requirements.txt
└── 📁 data/
    └── WatchAudio/       # Folder to drop audio files

 ```
## App Setup
We are seeting up the icon using .ico for windows and .icns for mac. 
 ```bash
pip install py2app
```
 ```bash
cd /path/to/audio\ mod
python3 setup.py py2app
```
This will generate:
 ```bash
dist/
└── Audio Profanity Tagger.app
 ```

## Running Code on a compiler
 ```bash
python ui.py
 ```




