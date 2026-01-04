from typing import Callable, Dict, Any, NamedTuple
from dataclasses import dataclass
import datetime

@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    safety_level: str = "SAFE" # SAFE, RISKY

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, name: str, description: str, safety_level: str = "SAFE"):
        def decorator(func):
            self._tools[name] = Tool(name, description, func, safety_level)
            return func
        return decorator

    def get_tool(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self) -> str:
        return "\n".join([f"- {t.name}: {t.description} ({t.safety_level})" for t in self._tools.values()])

    def execute(self, name: str, **kwargs):
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        return tool.func(**kwargs)

# Global Registry
registry = ToolRegistry()

# --- Basic Tools ---

@registry.register("get_current_time", "Returns the current system time")
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@registry.register("create_file", "Creates a file with content. RISKY if overwriting.", safety_level="RISKY")
def create_file(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)
    return f"File created at {path}"

@registry.register("chat_response", "Conversational response")
def chat_response(response_text: str = None):
    # This tool doesn't do much, the CLI handles the printing usually.
    # But returning the text allows CLI to see it as a result if it uses return value.
    if response_text:
        return response_text
    return "I am listening."
