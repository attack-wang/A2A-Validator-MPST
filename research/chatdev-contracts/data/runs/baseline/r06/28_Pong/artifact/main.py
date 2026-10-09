'''
main.py
Entry point for the two-player Pong game. Creates the Game object and
starts the main loop. If the 'pygame' dependency is missing, a clear
installation hint is printed instead of a raw traceback.
'''
import sys
def main():
    # Import lazily inside a guard so a missing dependency produces a
    # friendly, actionable message (ModuleNotFoundError is a subclass
    # of ImportError, so both cases are covered).
    try:
        from game import Game
    except ImportError:
        print("ERROR: the required dependency 'pygame' is not installed.")
        print("Install it with:            pip install pygame")
        print("Or install all dependencies: pip install -r requirements.txt")
        sys.exit(1)
    game = Game()
    game.run()
if __name__ == "__main__":
    main()