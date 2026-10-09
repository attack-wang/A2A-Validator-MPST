'''
Entry point for the Flappy Bird clone.
Catches a missing third-party dependency (pygame) at import time and
prints a clear installation hint instead of a raw ModuleNotFoundError
traceback, so the program fails gracefully in unprepared environments.
'''
import sys
try:
    from game import Game
except ImportError as exc:
    if getattr(exc, "name", "") == "pygame":
        print("ERROR: the required module 'pygame' is not installed.")
        print("Install it with:  pip install pygame")
        print("Or install all dependencies with:  pip install -r requirements.txt")
        sys.exit(1)
    raise
def main():
    """Create and run the game."""
    Game().run()
if __name__ == "__main__":
    main()