import google.generativeai as genai
import os
import json
from PIL import Image

class GeminiBrain:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.getenv("GENAI_API_KEY")
        
        if not api_key:
            print("[Brain] Warning: GENAI_API_KEY not found.")
            
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.system_prompt = """
        You are AMAR, a screen-aware desktop assistant.
        You receive a screenshot of the user's screen and their voice query.
        
        Your goal is to:
        1. Answer their question based on the screen visualization.
        2. OR Execute a system action if requested (like opening apps, typing, clicking).
        
        If an action is required, output STRICT JSON in this format:
        {"action": "open", "value": "app_name"}
        {"action": "type", "value": "text to type"}
        {"action": "key_combo", "value": ["ctrl", "c"]}
        {"action": "terminal", "value": "command"}
        
        If no action is needed, just return the plain text answer.
        DO NOT use markdown code blocks for JSON. Just the raw JSON string.
        """

    def analyze(self, image: Image.Image, text_query: str):
        """
        Sends image and text to Gemini.
        """
        print(f"[Brain] Analyzing Screen + Query: '{text_query}'")
        
        try:
            response = self.model.generate_content([self.system_prompt, text_query, image])
            return response.text.strip()
        except Exception as e:
            return f"Error from Gemini: {e}"

    def parse_response(self, response_text: str):
        """
        Heuristic to detect if response is JSON action or Text.
        """
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        if response_text.startswith("{") and response_text.endswith("}"):
            try:
                data = json.loads(response_text)
                return {"type": "action", "payload": data}
            except:
                pass
                
        return {"type": "text", "payload": response_text}
