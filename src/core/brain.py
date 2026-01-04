from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os
import re # Added regex support
from .decision import Decision, DecisionType

class Brain(ABC):
    @abstractmethod
    def think(self, history: List[Dict[str, str]]) -> Decision:
        """Process history and return a made decision."""
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Just generate text (for conversation)."""
        pass

from .chat import ChatEngine

class MockBrain(Brain):
    """
    Enhanced Regex-based Brain for Phase 3 & 4.
    """
    def __init__(self):
        self.chat_engine = ChatEngine()

    def think(self, history: List[Dict[str, str]]) -> Decision:
        last_msg = history[-1]['content'].lower()
        
        # --- PATTERNS ---

        # 1. Terminal / Shell
        if "terminal" in last_msg or "run command" in last_msg:
             # Smarter cleanup
             cmd = last_msg
             for stop in ["terminal", "se", "run", "command", "kro", "please"]:
                 cmd = cmd.replace(stop, "")
             cmd = cmd.strip()
             
             return Decision(
                type=DecisionType.PAUSE, 
                reason="User wants to run a terminal command.",
                question=f"Should I run '{cmd}' in the terminal?",
                action_plan="run_terminal_command",
                action_args={"command": cmd}
            )

        # 2. WhatsApp
        if "whatsapp" in last_msg and ("send" in last_msg or "bhejo" in last_msg):
            return Decision(
                type=DecisionType.PAUSE,
                reason="User wants to send a WhatsApp message.",
                question="Proceed with WhatsApp automation?",
                action_plan="send_whatsapp", 
                action_args={"contact_name": "Unknown", "message": "Draft Message"} 
            )

        # 3. Web Search
        if "search" in last_msg or "dhoondo" in last_msg or "google" in last_msg:
             query = last_msg 
             # Remove noise words to isolate query
             for stop in ["search", "google", "kro", "please", "dhoondo", "for", "pe", "ka", "bta", "btao"]:
                 query = query.replace(stop, "")
             query = query.strip()
             
             return Decision(
                type=DecisionType.ACT,
                reason=f"Searching for {query}",
                action_plan="web_search",
                action_args={"query": query}
            )

        # 4. Open App (Enhanced Logic)
        if "open" in last_msg or "kholo" in last_msg:
             app = last_msg
             # Stop at prepositions to avoid "mail on chrome" -> "mail on chrome"
             # Instead "chrome pe mail" -> "chrome" (if logic reverses) OR just extracting known app nouns?
             # Simple approach: remove the verb and prepositions.
             for stop in ["open", "kholo", "please", "on", "mein", "pe"]:
                 app = app.replace(stop, " ") # Replace with space to avoid merging
             
             app = app.strip()
             
             return Decision(
                type=DecisionType.ACT,
                reason=f"Opening {app}",
                action_plan="open_application",
                action_args={"app_name": app}
            )
            
        # 5. Time
        if "time" in last_msg or "bja" in last_msg:
             return Decision(
                type=DecisionType.ACT,
                reason="Time check",
                action_plan="get_current_time"
            )

        # Default: Chat Personality
        reply = self.chat_engine.get_response(last_msg)
        return Decision(
            type=DecisionType.ACT,
            reason="Conversational",
            action_plan="chat_response",
            # We need a way to pass the generated reply. 
            # In Phase 2 CLI we used 'text' arg in chat_response as placeholder.
            # Let's verify CLI handling. CLI currently ignores args for chat_response and generates its own.
            # We need to change that.
            action_args={"response_text": reply} 
        )

    def generate_response(self, text: str) -> str:
        return self.chat_engine.get_response(text)
