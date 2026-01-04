import pyautogui
import speech_recognition as sr
import os
from datetime import datetime
from PIL import Image

class ScreenCapture:
    @staticmethod
    def capture_screen(save_path: str = None) -> Image.Image:
        """
        Captures the entire screen.
        If save_path is provided, saves the image there.
        Returns the PIL Image object.
        """
        screenshot = pyautogui.screenshot()
        if save_path:
            screenshot.save(save_path)
        return screenshot

class AudioCapture:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic_index = None
        # Try to find the good mic again (reusing logic from our previous fix)
        try:
             mics = sr.Microphone.list_microphone_names()
             for i, name in enumerate(mics):
                 if "microphone array" in name.lower() or "realtek" in name.lower():
                     if "mapper" not in name.lower():
                         self.mic_index = i
                         break
        except:
            pass

    def listen_once(self, timeout=5) -> str:
        """
        Listens for a single command and returns the transcribed text.
        """
        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print("[Audio] Listening...")
                # self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                print("[Audio] Processing...")
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"[Audio Error] {e}")
            return ""

if __name__ == "__main__":
    # Test
    print("Testing Screen Capture...")
    img = ScreenCapture.capture_screen("test_screen.png")
    print(f"Screenshot taken: {img.size}")
    
    print("Testing Audio (Say something)...")
    recorder = AudioCapture()
    text = recorder.listen_once()
    print(f"Heard: {text}")
