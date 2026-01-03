import sys
from src.interface.cli import CLI
# Import automation tools to register them
import src.tools.automation 
import src.tools.system_ops 

def main():
    use_voice = "--voice" in sys.argv
    app = CLI(use_voice=use_voice)
    app.start()

if __name__ == "__main__":
    main()
