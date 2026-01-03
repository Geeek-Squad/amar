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

class MockBrain(Brain):
    """
    Enhanced Regex-based Brain for Phase 3.
    """
    def think(self, history: List[Dict[str, str]]) -> Decision:
        last_msg = history[-1]['content'].lower()
        
        # --- PATTERNS ---

        # 1. Terminal / Shell (Explicit request)
        # "terminal se [command] run kro", "run [command]"
        if "terminal" in last_msg or "run command" in last_msg:
             # Extract command roughly
             cmd = last_msg.replace("terminal se", "").replace("run command", "").replace("run", "").replace("kro", "").strip()
             return Decision(
                type=DecisionType.PAUSE, # Always pause for shell
                reason="User wants to run a terminal command.",
                question=f"Should I run '{cmd}' in the terminal?",
                action_plan="run_terminal_command",
                action_args={"command": cmd}
            )

        # 2. WhatsApp (Hinglish: bhejo, send)
        if "whatsapp" in last_msg and ("send" in last_msg or "bhejo" in last_msg):
            # Try to find contact?
            return Decision(
                type=DecisionType.PAUSE,
                reason="User wants to send a WhatsApp message.",
                question="Proceed with WhatsApp automation?",
                action_plan="send_whatsapp", 
                action_args={"contact_name": "Unknown", "message": "Draft Message"} 
            )

        # 3. Web Search (Hinglish: dhoondo, search kro, google kro)
        if "search" in last_msg or "dhoondo" in last_msg or "google" in last_msg:
             # Extract query
             query = last_msg 
             for stop in ["search", "google", "kro", "please", "dhoondo", "for", "pe"]:
                 query = query.replace(stop, "")
             query = query.strip()
             
             return Decision(
                type=DecisionType.ACT,
                reason=f"Searching for {query}",
                action_plan="web_search",
                action_args={"query": query}
            )

        # 4. Open App (Hinglish: kholo, open)
        if "open" in last_msg or "kholo" in last_msg:
             app = last_msg.replace("open", "").replace("kholo", "").replace("please", "").strip()
             return Decision(
                type=DecisionType.ACT,
                reason=f"Opening {app}",
                action_plan="open_application",
                action_args={"app_name": app}
            )
            
        # 5. Time (Hinglish: time kya hai, kitna bja hai)
        if "time" in last_msg or "bja" in last_msg:
             return Decision(
                type=DecisionType.ACT,
                reason="Time check",
                action_plan="get_current_time"
            )

        # Default
        return Decision(
            type=DecisionType.ACT,
            reason="Conversational",
            action_plan="chat_response"
        )

    def generate_response(self, text: str) -> str:
        return f"[AMAR]: {text}"
