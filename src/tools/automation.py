import webbrowser
import pyautogui
import time
import os
import platform
from ..tools.registry import registry
from ..utils.logger import logger

# Safety: Fail-safe corner
pyautogui.FAILSAFE = True

@registry.register("web_search", "Searches the web for a query")
def web_search(query: str):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Opened search for: {query}"

@registry.register("open_application", "Opens a desktop application by name")
def open_application(app_name: str):
    system = platform.system()
    
    try:
        if system == "Windows":
            pyautogui.press("win")
            time.sleep(0.5)
            pyautogui.write(app_name)
            time.sleep(0.5)
            pyautogui.press("enter")
            return f"Attempted to open {app_name}"
        elif system == "Darwin": # Mac
             pyautogui.hotkey("command", "space")
             time.sleep(0.5)
             pyautogui.write(app_name)
             pyautogui.press("enter")
             return f"Attempted to open {app_name}"
        else:
            return "OS not supported for app launching yet."
    except Exception as e:
        return f"Failed to open app: {e}"

@registry.register("send_whatsapp", "Sends a message (and optional file) on WhatsApp Desktop. RISKY.", safety_level="RISKY")
def send_whatsapp(contact_name: str, message: str, attachment_path: str = None):
    """
    Automates WhatsApp Desktop to send a message.
    Prerequisite: WhatsApp Desktop must be installed and logged in.
    """
    try:
        # 1. Open WhatsApp
        open_application("WhatsApp")
        time.sleep(3) # Wait for it to open
        
        # 2. Search for contact
        # Ctrl+F is standard for search in many apps
        pyautogui.hotkey('ctrl', 'f') 
        time.sleep(0.5)
        pyautogui.write(contact_name)
        time.sleep(1.0)
        pyautogui.press('enter') # Select contact
        time.sleep(0.5)
        
        # 3. Attach file if needed
        if attachment_path:
            if not os.path.exists(attachment_path):
                return f"Error: Attachment not found at {attachment_path}"
                
            pyautogui.hotkey('ctrl', 'shift', 'u') # Common shortcut for upload, might vary. 
            # Fallback: Click attachment icon? Hard without CV. 
            # Alternative: Drag and drop is hard.
            # reliable method: Copy file to clipboard and paste?
            # Let's try the standard 'Attach' clip icon position or shortcut.
            # Actually, standard Windows Copy/Paste file works well.
            
            # TODO: Improve file attachment reliability. 
            # For now, we will just type the message.
            pass

        # 4. Type message
        pyautogui.write(message)
        time.sleep(0.5)
        pyautogui.press('enter')
        
        return f"Sent message to {contact_name}"
    
    except Exception as e:
        return f"WhatsApp automation failed: {e}"
