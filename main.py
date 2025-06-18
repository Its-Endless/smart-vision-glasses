import pyttsx3
from mode_manager import ModeManager
from config import settings

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    print("Enter your command:")
    speak("Enter your command:")
    command = input()  # Taking text input instead of voice input
    print(f"You said: {command}")
    return command

def parse_command(command):
    command = command.lower().strip()

    # Exit trigger
    if command in ["exit", "turn off", "shutdown", "stop"]:
        return "exit"

    # Remove hotword
    if command.startswith("hey vision"):
        command = command[len("hey vision"):].strip()

    # Remove filler words
    fillers = ["open", "switch to", "activate", "start", "turn on"]
    for filler in fillers:
        if command.startswith(filler):
            command = command[len(filler):].strip()
            break

    # Normalize mode aliases
    mode = settings.MODE_ALIASES.get(command, command)
    return mode

def main():
    mode_manager = ModeManager()

    while True:
        user_command = listen_for_command()
        if not user_command:
            continue

        mode_name = parse_command(user_command)

        if mode_name == "exit":
            speak("Shutting down. Goodbye!")
            print("Shutting down. Goodbye!")
            break

        mode_manager.switch_mode(mode_name)

if __name__ == "__main__":
    main()
