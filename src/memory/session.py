from dataclasses import dataclass, field
from typing import List, Dict, Any
import datetime

@dataclass
class Message:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

class Session:
    def __init__(self, user_id: str = "user"):
        self.user_id = user_id
        self.history: List[Message] = []
        self.context: Dict[str, Any] = {}
        self.current_task: str = None
    
    def add_message(self, role: str, content: str):
        self.history.append(Message(role=role, content=content))
    
    def get_history(self) -> List[Dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.history]
    
    def set_context(self, key: str, value: Any):
        self.context[key] = value
        
    def get_context(self, key: str):
        return self.context.get(key)
    
    def clear_history(self):
        self.history = []

