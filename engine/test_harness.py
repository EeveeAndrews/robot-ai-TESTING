import time
from engine.t_main import process_input

class Session:
    def __init__(self):
        self.current_state = "IDLE"
        self.state_entered_at = time.time()

def run():
    session = Session()
    print("Type messages to the robot. Ctrl+C to quit.\n")
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        response = process_input(user_input, session)
        print(f"Robot ({response['state']}): {response['speech']}\n")

if __name__ == "__main__":
    run()
