import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io
import os
from typing import Optional

class VoiceEngine:
    def __init__(self, voice_id: Optional[str] = None):
        # Initialize TTS (Speech Synthesis)
        try:
            self.tts_engine = pyttsx3.init()
            if voice_id:
                self.tts_engine.setProperty('voice', voice_id)
            self.tts_engine.setProperty('rate', 180)  # Professional AI speed
        except Exception as e:
            print(f"🔴 TTS Initialization Error: {e}")
            self.tts_engine = None

        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000  # Standard for speech recognition

    def speak(self, text: str):
        """Converts text to speech."""
        if not self.tts_engine:
            print(f"🔊 AI: {text}")
            return
        
        print(f"🔊 J.A.R.V.I.S: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self) -> Optional[str]:
        """
        Listens using sounddevice (no PyAudio required) 
        and converts to text via SpeechRecognition.
        """
        print("👂 Listening (JARVIS is attentive)...")
        duration = 5  # Capture 5 seconds of audio
        
        try:
            # Record audio using sounddevice (numpy array)
            recording = sd.rec(int(duration * self.sample_rate), 
                              samplerate=self.sample_rate, 
                              channels=1, 
                              dtype='int16')
            sd.wait()  # Wait until recording is finished
            
            # Convert numpy array to WAV bytes in memory
            byte_io = io.BytesIO()
            wav.write(byte_io, self.sample_rate, recording)
            byte_io.seek(0)
            
            # Use SpeechRecognition to read the WAV bytes
            with sr.AudioFile(byte_io) as source:
                audio_data = self.recognizer.record(source)
                print("⌛ Identifying...")
                text = self.recognizer.recognize_google(audio_data)
                print(f"👂 Recognized: {text}")
                return text
                
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"🔴 Voice Input Error: {e}")
            return None
