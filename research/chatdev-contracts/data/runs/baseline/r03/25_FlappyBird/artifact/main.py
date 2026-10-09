'''
Entry point for the Flappy Bird clone. Run this file to play.
Fix: catches a missing 'pygame' dependency (ModuleNotFoundError reported in
the test) and prints clear installation instructions instead of a raw
traceback, so the program always exits gracefully with actionable guidance.
'''
import sys
try:
    from game import Game
except ModuleNotFoundError as exc:
    if exc.name == "pygame":
        print("ERROR: the required dependency 'pygame' is not installed.")
        print("Install it with one of the following commands:")
        print("    pip install pygame")
        print("    pip install -r requirements.txt")
        sys.exit(1)
    raise
def main():
    """Create the Game instance and start the main loop."""
    Game().run()
if __name__ == "__main__":
    main()