import pyttsx3

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    for index, voice in enumerate(voices):
        print(f"Index: {index}")
        print(f"ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Languages: {voice.languages}")
        print("-" * 20)

if __name__ == "__main__":
    list_voices()
