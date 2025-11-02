"""
Speech-to-text processing using OpenAI Whisper
"""

import os
from typing import Optional

# Try to import whisper, but handle gracefully if not available
try:
    import whisper
    WHISPER_AVAILABLE = True
except (ImportError, TypeError, AttributeError, Exception) as e:
    WHISPER_AVAILABLE = False
    whisper = None  # Set to None if import fails


class SpeechProcessor:
    """Service for processing audio to text"""
    
    def __init__(self):
        self.model = None
        self.model_size = "base"  # Options: tiny, base, small, medium, large
    
    def _load_model(self):
        """Load Whisper model (called lazily)"""
        if not WHISPER_AVAILABLE or whisper is None:
            print("[WARN] Whisper not available (not installed or unsupported Python version)")
            print("Speech-to-text will be disabled")
            self.model = None
            return
            
        if self.model is None:
            print(f"Loading Whisper model ({self.model_size})...")
            try:
                self.model = whisper.load_model(self.model_size)
                print("[OK] Whisper model loaded")
            except Exception as e:
                print(f"[WARN] Could not load Whisper model: {e}")
                print("Speech-to-text will be disabled")
                self.model = None
    
    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load model if not already loaded
        if self.model is None:
            self._load_model()
        
        if self.model is None:
            return "Speech transcription unavailable"
        
        try:
            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                language="en",  # Can be auto-detected
                task="transcribe"
            )
            
            return result["text"].strip()
        
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return "Error: Could not transcribe audio"
    
    async def transcribe_with_timestamps(self, audio_path: str):
        """
        Transcribe audio with word-level timestamps
        
        Returns:
            Dict with segments containing text and timestamps
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        if self.model is None:
            self._load_model()
        
        if self.model is None:
            return {"segments": []}
        
        try:
            result = self.model.transcribe(
                audio_path,
                word_timestamps=True
            )
            
            return result
        
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return {"segments": []}


