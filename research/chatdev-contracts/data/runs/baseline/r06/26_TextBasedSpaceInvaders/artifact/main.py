'''
main.py - Entry point for the Space Invaders game.
Catches a missing third-party dependency (pygame) at import time and
prints an actionable installation hint instead of a raw traceback.
'''
import sys
try:
    from game import Game
except ModuleNotFoundError as exc:
    # pygame is the only third-party dependency of this project;
    # give the user a clear, actionable message if it is absent.
    if getattr(exc, "name", "") == "pygame":
        print("ERROR: the 'pygame' module is required but not installed.")
        print("Install it with:  pip install pygame")
        sys.exit(1)
    raise
def main():
    """Create the Game instance and start the main loop."""
    game = Game()
    game.run()
if __name__ == "__main__":
    main()