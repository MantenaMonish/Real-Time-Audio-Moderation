# tagger.py

import whisper
import re
from better_profanity import profanity

# Load the Whisper model and profanity word list once
model = whisper.load_model("small")
profanity.load_censor_words()

def transcribe_audio(file_path):
    """Transcribes audio using Whisper"""
    result = model.transcribe(file_path)
    return result["text"].strip()

def detect_profanity(text):
    """Detects profanity in transcribed text"""
    if profanity.contains_profanity(text):
        if len(re.findall(r'\b[a-zA-Z]{4,}\b', text)) > 3:
            return "explicit"
        else:
            return "mild"
    return "clean"

def process_audio(file_path):
    print(f"Processing audio: {file_path}")  # Debug print
    transcript = transcribe_audio(file_path)
    print(f"Transcript: {transcript}")  # Debug print
    tag = detect_profanity(transcript)
    print(f"Tag: {tag}")  # Debug print
    return {
        "file": file_path,
        "transcript": transcript,
        "tag": tag
    }

