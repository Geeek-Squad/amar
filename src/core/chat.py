import random

class ChatEngine:
    def __init__(self):
        # Basic Knowledge Base
        self.responses = {
            "greeting": [
                "Hello! Main AMAR hun. Bataiye kya kar sakta hun?",
                "Namaste! I am read. Aaj kya plan hai?",
                "Hi there! Main sun raha hun."
            ],
            "feeling_good": [
                "Sunke accha laga! Positivity maintain rakhna zaroori hai.",
                "Great! Jab mood accha ho to kaam bhi badhiya hota hai.",
            ],
            "feeling_bad": [
                "Oh, I understand. Kabhi kabhi downtime bhi zaroori hai. Take a break if needed.",
                "Main sirf ek AI hun, par main sun sakta hun. Kya hua?",
                "Hmm. Koi baat nahi. Stress mat lijiye, sab thik ho jayega."
            ],
            "who_are_you": [
                "Main AMAR hun - aapka personal AI companion. Main robot nahi, aapka dost hun.",
                "I am AMAR. Main sochta hun, samajhta hun, aur execute karta hun."
            ],
            "default": [
                "Hmm...",
                "Achha, samajh gaya.",
                "Main sun raha hun, continue kijiye.",
                "Interesting."
            ]
        }

    def get_response(self, text: str) -> str:
        text = text.lower()
        
        # Greetings
        if any(w in text for w in ["hi", "hello", "namaste", "hey"]):
             return random.choice(self.responses["greeting"])
        
        # Identity
        if "who are you" in text or "kaun ho" in text:
            return random.choice(self.responses["who_are_you"])

        # Feelings (User)
        if "kaisa hai" in text or "how are you" in text:
            return "Main badhiya hun! Systems optimal hain. Aap kaise hain?"
            
        if "sad" in text or "udaas" in text or "bura" in text:
             return random.choice(self.responses["feeling_bad"])
             
        if "happy" in text or "khush" in text or "good" in text:
             return random.choice(self.responses["feeling_good"])
        # Philosophical / Open ended defaults
        return random.choice(self.responses["default"])
