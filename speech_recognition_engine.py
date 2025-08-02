#!/usr/bin/env python3
"""
Speech Recognition Engine with Whisper Integration
Real-time speech-to-text with CPU protection and multiple language support
"""

import json
import os
import time
import wave
import struct
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from cpu_manager import get_cpu_manager
import numpy as np

class WhisperEngine:
    """
    Whisper-based speech recognition engine with CPU protection
    """
    
    def __init__(self):
        # Initialize CPU manager
        self.cpu_manager = get_cpu_manager(max_cpu=80.0)
        
        # Whisper configuration
        self.config = {
            "model": "base",  # tiny, base, small, medium, large
            "language": "en",
            "task": "transcribe",
            "temperature": 0,
            "sample_rate": 16000,
            "chunk_length": 30,  # seconds
            "vad_threshold": 0.5,  # Voice activity detection threshold
            "energy_threshold": 1000,
            "pause_threshold": 0.8,
            "phrase_threshold": 0.3,
            "dynamic_energy": True
        }
        
        # Model sizes and performance
        self.model_specs = {
            "tiny": {"size": "39M", "speed": 32, "accuracy": 0.7},
            "base": {"size": "74M", "speed": 16, "accuracy": 0.8},
            "small": {"size": "244M", "speed": 8, "accuracy": 0.85},
            "medium": {"size": "769M", "speed": 4, "accuracy": 0.9},
            "large": {"size": "1550M", "speed": 2, "accuracy": 0.95}
        }
        
        # Audio buffer
        self.audio_buffer = []
        self.is_recording = False
        self.is_processing = False
        
        # Recognition state
        self.current_transcript = ""
        self.full_transcript = []
        self.confidence_scores = []
        
        # Language detection
        self.detected_languages = []
        self.language_probabilities = {}
        
        # Performance metrics
        self.metrics = {
            "total_audio_processed": 0,
            "average_processing_time": 0,
            "accuracy_score": 0,
            "cpu_usage_average": 0
        }
    
    def initialize_model(self, model_size: str = "base"):
        """
        Initialize Whisper model with specified size
        """
        print(f"Initializing Whisper model: {model_size}")
        
        # Check CPU before loading model
        self.cpu_manager.wait_for_cpu()
        
        # Simulate model loading (in production, load actual Whisper model)
        model_info = self.model_specs.get(model_size, self.model_specs["base"])
        
        print(f"  Model size: {model_info['size']}")
        print(f"  Processing speed: {model_info['speed']}x realtime")
        print(f"  Expected accuracy: {model_info['accuracy']*100}%")
        
        self.config["model"] = model_size
        
        # Simulate initialization delay
        time.sleep(0.5)
        
        print("✓ Model loaded successfully")
        
        return True
    
    def transcribe_audio(self, audio_data: bytes, language: str = None) -> Dict:
        """
        Transcribe audio data to text
        """
        # Check CPU before processing
        self.cpu_manager.wait_for_cpu()
        
        # Start processing
        self.is_processing = True
        start_time = time.time()
        
        # Prepare audio for transcription
        audio_array = self._prepare_audio(audio_data)
        
        # Detect language if not specified
        if not language:
            language = self._detect_language(audio_array)
        
        # Transcribe with CPU throttling
        result = self.cpu_manager.throttled_execute(
            self._whisper_transcribe,
            audio_array,
            language
        )
        
        # Calculate metrics
        processing_time = time.time() - start_time
        self._update_metrics(len(audio_data), processing_time)
        
        self.is_processing = False
        
        return result
    
    def _prepare_audio(self, audio_data: bytes) -> np.ndarray:
        """
        Prepare audio data for Whisper processing
        """
        # Convert bytes to numpy array
        # In production, properly decode audio format
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Normalize audio
        audio_array = audio_array.astype(np.float32) / 32768.0
        
        # Resample if needed
        if self.config["sample_rate"] != 16000:
            audio_array = self._resample_audio(audio_array)
        
        return audio_array
    
    def _resample_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Resample audio to 16kHz for Whisper
        """
        # Simple resampling (in production, use proper resampling)
        return audio
    
    def _detect_language(self, audio: np.ndarray) -> str:
        """
        Detect language from audio
        """
        # Simulate language detection
        # In production, use Whisper's language detection
        
        detected = {
            "en": 0.95,
            "es": 0.02,
            "fr": 0.02,
            "de": 0.01
        }
        
        self.language_probabilities = detected
        
        # Return most probable language
        return max(detected, key=detected.get)
    
    def _whisper_transcribe(self, audio: np.ndarray, language: str) -> Dict:
        """
        Core Whisper transcription
        """
        # Simulate Whisper transcription
        # In production, use actual Whisper model
        
        # Simulate processing delay based on model size
        model_speed = self.model_specs[self.config["model"]]["speed"]
        processing_delay = len(audio) / self.config["sample_rate"] / model_speed
        
        # Apply CPU-safe delay
        self.cpu_manager.adaptive_sleep(min(processing_delay, 0.5))
        
        # Generate mock transcription
        result = {
            "text": "This is a simulated transcription of the audio input.",
            "segments": [
                {
                    "id": 1,
                    "start": 0.0,
                    "end": 3.0,
                    "text": "This is a simulated",
                    "confidence": 0.92
                },
                {
                    "id": 2,
                    "start": 3.0,
                    "end": 6.0,
                    "text": "transcription of the audio input.",
                    "confidence": 0.88
                }
            ],
            "language": language,
            "duration": len(audio) / self.config["sample_rate"],
            "confidence": 0.9
        }
        
        # Update transcript
        self.current_transcript = result["text"]
        self.full_transcript.append(result["text"])
        self.confidence_scores.append(result["confidence"])
        
        return result
    
    def transcribe_file(self, file_path: str) -> Dict:
        """
        Transcribe audio file
        """
        print(f"Transcribing file: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        # Read audio file
        try:
            with open(file_path, 'rb') as f:
                audio_data = f.read()
        except Exception as e:
            return {"error": f"Failed to read file: {e}"}
        
        # Transcribe
        return self.transcribe_audio(audio_data)
    
    def start_realtime_transcription(self):
        """
        Start real-time transcription from microphone
        """
        print("Starting real-time transcription...")
        print("Speak into your microphone (Press Ctrl+C to stop)")
        
        self.is_recording = True
        
        # Start recording thread
        recording_thread = threading.Thread(target=self._record_audio, daemon=True)
        recording_thread.start()
        
        # Start transcription thread
        transcription_thread = threading.Thread(target=self._process_audio_stream, daemon=True)
        transcription_thread.start()
        
        return True
    
    def _record_audio(self):
        """
        Record audio from microphone
        """
        # Simulate audio recording
        # In production, use actual microphone input
        
        while self.is_recording:
            # Check CPU
            self.cpu_manager.wait_for_cpu()
            
            # Simulate audio chunk
            chunk = self._simulate_audio_chunk()
            
            # Add to buffer
            self.audio_buffer.append(chunk)
            
            # Adaptive sleep
            self.cpu_manager.adaptive_sleep(0.1)
    
    def _simulate_audio_chunk(self) -> bytes:
        """
        Simulate audio chunk for testing
        """
        # Generate silence or noise
        duration = 0.1  # 100ms chunks
        sample_rate = self.config["sample_rate"]
        num_samples = int(duration * sample_rate)
        
        # Generate random audio data
        samples = np.random.randint(-1000, 1000, num_samples, dtype=np.int16)
        
        return samples.tobytes()
    
    def _process_audio_stream(self):
        """
        Process audio stream in real-time
        """
        chunk_buffer = []
        chunk_duration = 0
        
        while self.is_recording:
            if self.audio_buffer:
                # Get audio chunk
                chunk = self.audio_buffer.pop(0)
                chunk_buffer.append(chunk)
                chunk_duration += 0.1  # Assuming 100ms chunks
                
                # Process when we have enough audio
                if chunk_duration >= self.config["chunk_length"]:
                    # Combine chunks
                    combined_audio = b''.join(chunk_buffer)
                    
                    # Transcribe
                    result = self.transcribe_audio(combined_audio)
                    
                    # Display result
                    if result.get("text"):
                        print(f"\n📝 Transcription: {result['text']}")
                        print(f"   Confidence: {result.get('confidence', 0):.2%}")
                    
                    # Reset buffer
                    chunk_buffer = []
                    chunk_duration = 0
            
            # Small delay
            time.sleep(0.01)
    
    def stop_realtime_transcription(self):
        """
        Stop real-time transcription
        """
        print("\nStopping transcription...")
        self.is_recording = False
        
        # Process remaining audio
        if self.audio_buffer:
            remaining = b''.join(self.audio_buffer)
            if remaining:
                result = self.transcribe_audio(remaining)
                if result.get("text"):
                    print(f"\nFinal: {result['text']}")
        
        # Clear buffer
        self.audio_buffer.clear()
        
        print("Transcription stopped")
        
        return self.get_full_transcript()
    
    def get_full_transcript(self) -> str:
        """
        Get complete transcript
        """
        return " ".join(self.full_transcript)
    
    def get_metrics(self) -> Dict:
        """
        Get performance metrics
        """
        return {
            "total_audio_processed": f"{self.metrics['total_audio_processed'] / 1024 / 1024:.2f} MB",
            "average_processing_time": f"{self.metrics['average_processing_time']:.2f} seconds",
            "average_confidence": f"{np.mean(self.confidence_scores) if self.confidence_scores else 0:.2%}",
            "cpu_usage": f"{self.cpu_manager.current_cpu_usage:.1f}%",
            "model": self.config["model"],
            "language": self.config["language"]
        }
    
    def _update_metrics(self, audio_size: int, processing_time: float):
        """
        Update performance metrics
        """
        self.metrics["total_audio_processed"] += audio_size
        
        # Update average processing time
        if self.metrics["average_processing_time"] == 0:
            self.metrics["average_processing_time"] = processing_time
        else:
            self.metrics["average_processing_time"] = (
                self.metrics["average_processing_time"] + processing_time
            ) / 2
    
    def set_language(self, language: str):
        """
        Set transcription language
        """
        self.config["language"] = language
        print(f"Language set to: {language}")
    
    def adjust_energy_threshold(self, threshold: int):
        """
        Adjust voice detection energy threshold
        """
        self.config["energy_threshold"] = threshold
        print(f"Energy threshold set to: {threshold}")
    
    def enable_auto_language_detection(self):
        """
        Enable automatic language detection
        """
        self.config["language"] = None
        print("Auto language detection enabled")


class MultiLanguageTranscriber:
    """
    Multi-language transcription support
    """
    
    def __init__(self):
        self.supported_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese"
        }
        
        self.engine = WhisperEngine()
    
    def transcribe_multilingual(self, audio_data: bytes) -> Dict:
        """
        Transcribe audio with automatic language detection
        """
        # Detect language
        detected_lang = self._detect_language_from_audio(audio_data)
        
        # Transcribe in detected language
        result = self.engine.transcribe_audio(audio_data, detected_lang)
        
        # Add language info
        result["detected_language"] = self.supported_languages.get(
            detected_lang, 
            detected_lang
        )
        
        return result
    
    def _detect_language_from_audio(self, audio_data: bytes) -> str:
        """
        Detect language from audio
        """
        # Use Whisper's language detection
        # For now, return default
        return "en"
    
    def translate_to_english(self, audio_data: bytes, source_language: str = None) -> Dict:
        """
        Transcribe and translate to English
        """
        # First transcribe in original language
        if not source_language:
            source_language = self._detect_language_from_audio(audio_data)
        
        result = self.engine.transcribe_audio(audio_data, source_language)
        
        # Translate to English (in production, use translation API)
        result["translation"] = f"[Translated from {source_language}]: {result.get('text', '')}"
        
        return result


class VoiceActivityDetector:
    """
    Detect voice activity in audio stream
    """
    
    def __init__(self):
        self.energy_threshold = 1000
        self.silence_threshold = 0.5
        self.speaking = False
        self.silence_duration = 0
    
    def is_speech(self, audio_chunk: bytes) -> bool:
        """
        Detect if audio chunk contains speech
        """
        # Convert to numpy array
        audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
        
        # Calculate energy
        energy = np.sqrt(np.mean(audio_array**2))
        
        # Check if energy exceeds threshold
        is_speech = energy > self.energy_threshold
        
        # Update state
        if is_speech:
            self.speaking = True
            self.silence_duration = 0
        else:
            self.silence_duration += 0.1  # Assuming 100ms chunks
            
            if self.silence_duration > self.silence_threshold:
                self.speaking = False
        
        return is_speech
    
    def adjust_threshold_dynamically(self, ambient_noise: float):
        """
        Adjust threshold based on ambient noise
        """
        self.energy_threshold = ambient_noise * 1.5
    
    def get_state(self) -> Dict:
        """
        Get current VAD state
        """
        return {
            "speaking": self.speaking,
            "energy_threshold": self.energy_threshold,
            "silence_duration": self.silence_duration
        }


if __name__ == "__main__":
    # Test speech recognition engine
    print("Testing Whisper Speech Recognition Engine...")
    print("="*50)
    
    # Initialize engine
    engine = WhisperEngine()
    
    # Initialize model
    engine.initialize_model("base")
    
    # Test file transcription
    print("\nTest 1: File Transcription")
    print("-"*30)
    
    # Simulate audio file
    test_audio = np.random.bytes(16000 * 5)  # 5 seconds of audio
    result = engine.transcribe_audio(test_audio)
    
    print(f"Transcription: {result.get('text', 'No transcription')}")
    print(f"Confidence: {result.get('confidence', 0):.2%}")
    print(f"Language: {result.get('language', 'Unknown')}")
    
    # Test metrics
    print("\nPerformance Metrics:")
    print("-"*30)
    metrics = engine.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Speech recognition engine test complete!")