# AMAR - Personal AI Assistant

AMAR is a "thinking companion" designed to act, ask, or pause based on intelligent decision making. It is NOT a simple chatbot.

## Architecture

The system is built on a modular architecture:

- **Brain (`src/core/brain.py`)**: The reasoning core. Currently a `MockBrain` for testing, but designed to be replaced by an LLM adapter.
- **Decision Engine (`src/core/decision.py`)**: Enforces the `ACT`, `ASK`, `PAUSE` logic.
- **Memory (`src/memory/session.py`)**: Manages conversation history and state.
- **Tools (`src/tools/registry.py`)**: A safe registry of executable actions.
- **Interface (`src/interface/cli.py`)**: The user-facing CLI loop.

## Usage

To start AMAR (Text Mode):
```bash
python main.py
```

To start AMAR (Voice Mode):
```bash
python main.py --voice
```

### Example Interaction

```text
[AMAR]: Hello. I am ready to assist.

[USER]: Google pe latest news search kro
[AMAR]: ...
[AMAR]: Executing web_search...
[AMAR]: Done. Result: Opened search for: latest news

[USER]: Terminal se ipconfig run kro
[AMAR]: ...
[AMAR]: Wait. User wants to run a terminal command.
[AMAR]: Should I run 'ipconfig' in the terminal? (y/n)
[USER]: y
[AMAR]: Action Completed. Output: ...

[USER]: Notepad kholo please
[AMAR]: ...
[AMAR]: Attempted to open notepad
```

## Setup

1. Requirements: Python 3.8+
2. Install Core Dependencies:
   ```bash
   pip install SpeechRecognition pyttsx3 pyautogui pyaudio
   ```

## Updates (Phase 3)
- **Hinglish Support**: Understands "kro", "bhejo", "dhoondo".
- **Terminal Control**: Can run shell commands (with confirmation).
- **Better Voice**: Tuned for clarity (Zira).

## Future Roadmap

- [ ] Connect real LLM API (OpenAI/Anthropic)
- [ ] Add persistence (SQLite/JSON)
- [ ] Add more system tools (File operations, Web search)
