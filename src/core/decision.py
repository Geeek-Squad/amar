from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class DecisionType(Enum):
    ACT = "ACT"      # Clear intent, safe to execute
    ASK = "ASK"      # Ambiguous, missing info, or unsure
    PAUSE = "PAUSE"  # Risky, requires explicit confirmation

@dataclass
class Decision:
    type: DecisionType
    reason: str
    action_plan: Optional[str] = None
    action_args: Dict[str, Any] = None
    question: Optional[str] = None
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH

