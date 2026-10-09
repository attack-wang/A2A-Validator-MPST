'''
main.py
Entry point for the two-player Pong game.
The pygame dependency is imported inside a guarded block so that a
missing installation produces a clear, actionable installation hint
instead of an unhandled ModuleNotFoundError traceback.
'''
import sys
try:
    from game import Game
except ImportError as exc:
    missing = getattr(exc, "name", "")
    if missing == "pygame":
        sys.stderr.write(
            "ERROR: the 'pygame' module is required to run this game "
            "but it is not installed.\n"
            "Install it with:\n"
            "    pip install pygame\n"
            "or install every dependency at once with:\n"
            "    pip install -r requirements.txt\n"
        )
    else:
        sys.stderr.write(
            "ERROR: missing dependency '{}'. "
            "Install it before running the game.\n".format(missing or exc)
        )
    sys.exit(1)
def main():
    """Create the Game instance and run the main loop."""
    game = Game()
    game.run()
if __name__ == "__main__":
    main()