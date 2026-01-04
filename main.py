import time
import os
import sys
from pynput import keyboard
from src.capture import ScreenCapture, AudioCapture
from src.core.brain_v2 import GeminiBrain
from src.actions import ActionExecutor
from dotenv import load_dotenv
import pyttsx3

# Load env for API Key
load_dotenv()

class AmarAssistant:
    def __init__(self):
        self.brain = GeminiBrain()
        self.audio_recorder = AudioCapture()
        self.tts = pyttsx3.init()
        self.is_listening = False
        
        # Configure voice
        voices = self.tts.getProperty('voices')
        if len(voices) > 1: self.tts.setProperty('voice', voices[1].id)
        self.tts.setProperty('rate', 160)

    def speak(self, text):
        print(f"[AMAR]: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

    def on_activate(self):
        """
        Triggered when hotkey is pressed.
        """
        print("\n--- Hotkey Triggered ---")
        self.speak("Listening")
        
        # 1. Capture Screen
        print("[System] Capturing Screen...")
        screenshot = ScreenCapture.capture_screen()
        
        # 2. Listen to Audio (Blocking for now, simpler)
        user_query = self.audio_recorder.listen_once(timeout=5)
        
        if not user_query:
            self.speak("I didn't hear anything.")
            return

        print(f"[User]: {user_query}")
        self.speak("Thinking")
        
        # 3. Brain Analysis
        response_text = self.brain.analyze(screenshot, user_query)
        parsed = self.brain.parse_response(response_text)
        
        # 4. Execute
        if parsed['type'] == 'action':
            action_data = parsed['payload']
            print(f"[Action Plan]: {action_data}")
            result = ActionExecutor.execute(action_data)
            self.speak(f"Done. {result}")
        else:
            reply = parsed['payload']
            self.speak(reply)

def start_listener():
    app = AmarAssistant()
    
    # Define Hotkey: Ctrl + Alt + s
    # We use GlobalHotKeys for convenience
    print("AMAR V2 Screen-Aware Assistant Online.")
    print("Press <Ctrl>+<Alt>+<s> to trigger...")
    
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+s': app.on_activate
    }) as h:
        h.join()

if __name__ == "__main__":
    start_listener()
