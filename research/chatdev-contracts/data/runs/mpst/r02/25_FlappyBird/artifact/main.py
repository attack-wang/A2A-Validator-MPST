'''
Entry point for the Flappy Bird clone.
Launches the Game. If a required dependency (e.g. pygame) is not installed,
a clear installation hint is printed instead of an opaque traceback, so the
user knows exactly how to get the game running.
'''
import sys
def main():
    """Start the game, or explain how to install missing dependencies."""
    try:
        # Import lazily so a missing dependency can be reported gracefully.
        from game import Game
    except ImportError as exc:
        missing = getattr(exc, "name", None) or "a required module"
        print("=" * 56)
        print("Could not start Flappy Bird: missing module '{}'".format(missing))
        print()
        print("Install the dependencies with:")
        print("    pip install -r requirements.txt")
        print("or directly:")
        print("    pip install pygame")
        print()
        print("Then run the game again with:")
        print("    python main.py")
        print("=" * 56)
        sys.exit(1)
    Game().run()
if __name__ == "__main__":
    main()