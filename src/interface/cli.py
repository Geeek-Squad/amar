import sys
import time
from typing import Optional, Dict, Any
from ..core.brain import MockBrain, Decision, DecisionType
from ..tools.registry import registry
from ..memory.session import Session
from ..utils.logger import logger
from src.interface.voice import VoiceInterface

class CLI:
    def __init__(self, use_voice: bool = False):
        self.brain = MockBrain()
        self.session = Session()
        self.voice = VoiceInterface() if use_voice else None
        self.running = True

    def type_out(self, text: str, delay: float = 0.01):
        """Simulate natural typing + Speak if enabled."""
        if self.voice:
            # Speak asynchronously or synchronously? 
            # Depending on pyttsx3, sync might block. Assuming sync for now.
            # We print first, then speak.
            pass

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        
        if self.voice:
             self.voice.speak(text)


    def start(self):
        print("\n" + "="*40)
        print(" AMAR SYSTEM ONLINE ".center(40, "="))
        print("="*40 + "\n")
        
        greeting = "Hello. I am ready to assist. Type or press Enter to speak."
        self.type_out(f"[AMAR]: {greeting}")
        
        while self.running:
            try:
                user_input = input("\n[USER] (Text/Enter for Voice): ").strip()
                
                # Voice Trigger
                if not user_input and self.voice:
                    user_input = self.voice.listen()
                    if user_input:
                        print(f"I heard: {user_input}")
                    else:
                        print("(No speech detected)")
                        continue

                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self.type_out("[AMAR]: Shutting down. Goodbye.")
                    self.running = False
                    break

                self.session.add_message("user", user_input)
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n[AMAR]: Interrupted. Shutting down.")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                self.type_out(f"[AMAR]: System error encountered: {e}")

    def process_input(self, text: str):
        # 1. Think
        self.type_out("...", delay=0.1) # Thinking indicator
        decision = self.brain.think(self.session.get_history())
        
        # 2. Act based on decision
        if decision.type == DecisionType.ACT:
            if decision.action_plan == "chat_response":
                # Just chat
                response = f"I heard you say: '{text}'."
                self.type_out(f"[AMAR]: {response}")
            else:
                # Execute tool with args
                self.type_out(f"[AMAR]: Executing {decision.action_plan}...")
                try:
                    kwargs = decision.action_args or {}
                    result = registry.execute(decision.action_plan, **kwargs)
                    self.type_out(f"[AMAR]: Done. Result: {result}")
                    self.session.add_message("system", f"Tool {decision.action_plan} executed. Result: {result}")
                except Exception as e:
                     self.type_out(f"[AMAR]: Execution failed: {e}")

        elif decision.type == DecisionType.ASK:
            self.type_out(f"[AMAR]: {decision.question}")
            self.session.add_message("assistant", decision.question)

        elif decision.type == DecisionType.PAUSE:
            self.type_out(f"[AMAR]: Wait. {decision.reason}")
            self.type_out(f"[AMAR]: {decision.question} (y/n)")
            
            # For PAUSE, logic might need to be smarter, but simplistic strictly confirms here.
            confirm = input("[USER]: ").strip().lower()
            if confirm == 'y':
                self.type_out("[AMAR]: Proceeding explicitly.")
                try:
                    if decision.action_plan:
                        kwargs = decision.action_args or {}
                        result = registry.execute(decision.action_plan, **kwargs)
                        self.type_out(f"[AMAR]: Action Completed. {result}")
                except Exception as e:
                    self.type_out(f"[AMAR]: Failed: {e}")
            else:
                self.type_out("[AMAR]: Aborting action.")

