# pyrefly: ignore [missing-import]
import whisper
# pyrefly: ignore [missing-import]
import sounddevice as sd
import numpy as np
from scipy.io 
import wavfile
import tempfile
import os

class VoiceAgent:
    """Agent for handling voice input via local Whisper model."""
    
    def __init__(self, model_name: str = "base"):
        # Whisper has tiny, base, small, medium, large. 'base' is a good fast local trade-off.
        # It downloads the model automatically on first run.
        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:

            print(f"Error loading whisper model: {e}")
            self.model = None
        
    def record_audio(self, duration: int = 5, samplerate: int = 16000) -> str:
        """Records audio from the microphone for a given duration and saves to a temp file."""
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_file.close()
        wavfile.write(temp_file.name, samplerate, audio)
        return temp_file.name
        
    def transcribe(self, file_path: str) -> str:
        """Transcribes the audio file using Whisper."""
        if not self.model:
            return "Error: Whisper model not loaded."
            
        try:
            result = self.model.transcribe(file_path)
            return result["text"].strip()
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                
    def listen_and_transcribe(self, duration: int = 5) -> str:
        """Records from the mic and returns the transcribed text."""
        try:
            audio_path = self.record_audio(duration)
            text = self.transcribe(audio_path)
            return text
        except Exception as e:
            return f"Error during voice listening: {e}"
