import pyautogui
import os
import time
import platform
import subprocess

class ActionExecutor:
    @staticmethod
    def execute(action_plan: dict):
        """
        Executes an action based on a dictionary plan.
        Format: {"action": "open", "value": "notepad"}
        """
        action = action_plan.get("action")
        value = action_plan.get("value")
        
        print(f"[Action] Executing: {action} -> {value}")
        
        if action == "open":
            return ActionExecutor.open_app(value)
        elif action == "type":
            return ActionExecutor.type_text(value)
        elif action == "key_combo":
            return ActionExecutor.press_keys(value)
        elif action == "terminal":
            return ActionExecutor.run_terminal(value)
        
        return "Unknown action"

    @staticmethod
    def open_app(app_name):
        system = platform.system()
        try:
            if system == "Windows":
                pyautogui.press("win")
                time.sleep(0.3)
                pyautogui.write(app_name)
                time.sleep(0.5)
                pyautogui.press("enter")
            elif system == "Darwin":
                pyautogui.hotkey("command", "space")
                time.sleep(0.3)
                pyautogui.write(app_name)
                pyautogui.press("enter")
            return f"Opened {app_name}"
        except Exception as e:
            return f"Error opening app: {e}"

    @staticmethod
    def type_text(text):
        try:
            # Type naturally
            pyautogui.write(text, interval=0.01)
            return "Typed text"
        except Exception as e:
            return f"Error typing: {e}"

    @staticmethod
    def press_keys(keys_list):
        # inputs like ["ctrl", "c"]
        try:
            if isinstance(keys_list, str):
                keys_list = [keys_list]
            pyautogui.hotkey(*keys_list)
            return f"Pressed {keys_list}"
        except Exception as e:
            return f"Error pressing keys: {e}"

    @staticmethod
    def run_terminal(command):
        try:
            subprocess.Popen(command, shell=True)
            return f"Ran command: {command}"
        except Exception as e:
            return f"Error running command: {e}"
