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
            voices = self.engine.getProperty('voices')
            found_voice = False
            for voice in voices:
                if "zira" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    found_voice = True
                    break
            
            if not found_voice and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id) # Fallback to index 1

            self.engine.setProperty('rate', 160) # Slightly slower clearly

            # Set Default Sensitivity (Lower = More Sensitive)
            self.recognizer.energy_threshold = 300 
            self.recognizer.dynamic_energy_threshold = True

            # Find best microphone (Realtek / Microphone Array)
            self.mic_index = None # Default
            try:
                mics = sr.Microphone.list_microphone_names()
                print(f"[System] Available Microphones: {len(mics)}")
                for i, name in enumerate(mics):
                    # Prefer hardware mics over "Mapper"
                    if "microphone array" in name.lower() or "realtek" in name.lower():
                        if "mapper" not in name.lower():
                            self.mic_index = i
                            print(f"[System] Selected Microphone: {name} (Index {i})")
                            break
            except:
                pass

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

        # Candidates to try if the current one fails (Lazy init)
        if not hasattr(self, 'mic_candidates'):
            self.mic_candidates = []
            try:
                mics = sr.Microphone.list_microphone_names()
                for i, name in enumerate(mics):
                    if "microphone array" in name.lower() or "realtek" in name.lower():
                        if "mapper" not in name.lower():
                            self.mic_candidates.append(i)
                # Ensure current choice is first
                if self.mic_index in self.mic_candidates:
                    self.mic_candidates.remove(self.mic_index)
                self.mic_candidates.insert(0, self.mic_index if self.mic_index is not None else 0)
                # Remove duplicates and Nones
                self.mic_candidates = sorted(list(set([c for c in self.mic_candidates if c is not None])))
                print(f"[System] Microphone Candidates: {self.mic_candidates}")
            except:
                self.mic_candidates = [0]
        
        # Try listening
        text = self._listen_once(prompt)
        
        # If timeout/silence, and we have other candidates, Try switching!
        if text == "" and len(self.mic_candidates) > 1:
            print("[System] Silence detected. Attempting to switch microphone...")
            current_idx = self.mic_candidates.index(self.mic_index) if self.mic_index in self.mic_candidates else -1
            
            # Try next ones
            start_search = current_idx + 1
            if start_search < len(self.mic_candidates):
                next_cand = self.mic_candidates[start_search]
                print(f"[System] Switching to Microphone Index {next_cand}...")
                self.mic_index = next_cand
                return self.listen(prompt="Trying new mic...")
                
        return text

    def _listen_once(self, prompt):
        device_index = self.mic_index
        try:
            with sr.Microphone(device_index=device_index) as source:
                print(f"\n({prompt} on Mic {device_index})")
                # Fast calibration
                # self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=10)
                    print("(Audio captured. Processing...)")
                    try:
                        text = self.recognizer.recognize_google(audio)
                        print(f"(Heard: {text})")
                        return text
                    except sr.UnknownValueError:
                        print("(Could not understand audio)")
                        return " " # Return space to indicate signal but no words, avoiding switch
                    except sr.RequestError as e:
                        print(f"(Network/API Error: {e})")
                        return ""
                except sr.WaitTimeoutError:
                    print("(Timeout: No speech detected)")
                    return ""
        except Exception as e:
             print(f"(Mic Error: {e})")
             return ""
