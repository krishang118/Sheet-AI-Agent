"""
Audio Transcription Helper using Faster-Whisper
Handles speech-to-text conversion for voice input
"""
import os
import tempfile
from typing import Optional, Dict, Any
from pathlib import Path
import streamlit as st

class AudioTranscriber:
    """Handles audio transcription using Faster-Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the transcriber
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        
    @st.cache_resource
    def _get_model(_self, model_size: str):
        """
        Load and cache the Whisper model
        
        Note: Uses @st.cache_resource to load model only once
        """
        try:
            from faster_whisper import WhisperModel
            
            # Load model with CPU optimization
            model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8"  # Optimized for CPU
            )
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model: {str(e)}")
    
    def transcribe(self, audio_input) -> Dict[str, Any]:
        """
        Transcribe audio to text
        
        Args:
            audio_input: Either bytes or UploadedFile from st.audio_input
            
        Returns:
            Dict with keys:
                - success: bool
                - text: str (transcribed text)
                - error: str (error message if failed)
                - duration: float (audio duration in seconds)
        """
        # Handle UploadedFile from st.audio_input
        try:
            # Check if it's an UploadedFile object (has .read() method)
            if hasattr(audio_input, 'read'):
                audio_bytes = audio_input.read()
            else:
                audio_bytes = audio_input
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": f"Failed to read audio data: {str(e)}",
                "duration": 0
            }
        
        # Input validation
        if not audio_bytes or len(audio_bytes) == 0:
            return {
                "success": False,
                "text": "",
                "error": "No audio data received",
                "duration": 0
            }
        
        # Check minimum size (very rough check for ~0.5s at 16kHz)
        # WAV header is ~44 bytes, 0.5s at 16kHz mono = ~16000 bytes
        if len(audio_bytes) < 16000:
            return {
                "success": False,
                "text": "",
                "error": "Recording too short (minimum 0.5 seconds)",
                "duration": 0
            }
        
        temp_file = None
        try:
            # Load model (cached)
            if self.model is None:
                self.model = self._get_model(self.model_size)
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                temp_file = f.name
            
            # Transcribe
            segments, info = self.model.transcribe(
                temp_file,
                language="en",
                beam_size=5,
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(
                    min_silence_duration_ms=500
                )
            )
            
            # Extract text from segments
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())
            
            transcript = " ".join(text_parts).strip()
            
            # Validate output
            if not transcript or len(transcript) < 2:
                return {
                    "success": False,
                    "text": "",
                    "error": "No speech detected in recording",
                    "duration": info.duration
                }
            
            return {
                "success": True,
                "text": transcript,
                "error": None,
                "duration": info.duration
            }
            
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": f"Transcription failed: {str(e)}",
                "duration": 0
            }
        
        finally:
            # Clean up temp file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass

# Singleton instance
_transcriber_instance = None

def get_transcriber() -> AudioTranscriber:
    """Get or create the global transcriber instance"""
    global _transcriber_instance
    if _transcriber_instance is None:
        _transcriber_instance = AudioTranscriber(model_size="base")
    return _transcriber_instance
