import os
import torch
import whisper
from better_profanity import profanity
from typing import Dict

profanity.load_censor_words()

class AudioProcessor:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        self.model = whisper.load_model("medium", device=self.device)

    def transcribe_audio(self, file_path: str) -> str:
        if not self.model:
            self.load_model()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        result = self.model.transcribe(file_path, fp16=torch.cuda.is_available())
        return result["text"]

    def check_profanity(self, text: str) -> str:
        return "PROFANE" if profanity.contains_profanity(text) else "CLEAN"

def process_audio(file_path: str) -> Dict[str, str]:
    processor = AudioProcessor()
    try:
        transcript = processor.transcribe_audio(file_path)
        clean_transcript = transcript.strip().replace('\n', ' ')
        return {
            "tag": processor.check_profanity(clean_transcript.lower()),
            "transcript": clean_transcript
        }
    except Exception as e:
        return {
            "tag": "ERROR",
            "transcript": f"Processing failed: {str(e)}"
        }
