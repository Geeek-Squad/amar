import speech_recognition as sr
import pyttsx3
from ..utils.logger import logger

class VoiceInterface:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            
            # Configure voice: Prefer "Zira" (Female/Clearer) or "David"
            # In user's system, Index 1 is likely 'Microsoft Zira' or just US English
            found_voice = False
            for voice in voices:
                if "zira" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    found_voice = True
                    break
            
            if not found_voice and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id) # Fallback to index 1

            self.engine.setProperty('rate', 160) # Slightly slower clearly
        except Exception as e:
            logger.error(f"Failed to initialize Voice Engine: {e}")
            self.engine = None

    def speak(self, text: str):
        if not self.engine:
            return
        
        try:
            # Don't speak technical logs or excessive symbols
            clean_text = text.replace("[AMAR]:", "").replace("_", " ")
            self.engine.say(clean_text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Speech error: {e}")

    def listen(self, prompt: str = "Listening...") -> str:
        if not self.engine:
            return ""

        with sr.Microphone() as source:
            print(f"\n({prompt})")
            # Sensitivity Tweaks for better hearing
            self.recognizer.energy_threshold = 300  # Lower = more sensitive
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8   # Wait less before finalizing
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio) # Default English model handles Hinglish/Indian accents decently
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                logger.error(f"Listening error: {e}")
                return ""
