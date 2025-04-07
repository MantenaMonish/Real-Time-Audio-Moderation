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
        # If there are more than 3 words of 4+ letters, mark as explicit
        if len(re.findall(r'\b[a-zA-Z]{4,}\b', text)) > 3:
            return "explicit"
        else:
            return "mild"
    return "clean"

def process_audio(file_path):
    """Processes audio file and returns result"""
    transcript = transcribe_audio(file_path)
    tag = detect_profanity(transcript)
    return {
        "file": file_path,
        "transcript": transcript,
        "tag": tag
    }
