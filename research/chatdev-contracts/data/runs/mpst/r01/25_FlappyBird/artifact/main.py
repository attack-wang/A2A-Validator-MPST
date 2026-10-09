'''
Entry point for the Flappy Bird clone.
'''
import sys
def main():
    """Create and run the Flappy Bird game."""
    try:
        from game import Game
    except ImportError as exc:
        # Graceful handling when pygame (or another dependency) is missing,
        # e.g. ModuleNotFoundError: No module named 'pygame'
        print("=" * 60)
        print("Failed to start Flappy Bird: {}".format(exc))
        print("The 'pygame' module is required but not installed.")
        print("Install it with one of the following commands:")
        print("    pip install pygame")
        print("    pip install -r requirements.txt")
        print("=" * 60)
        sys.exit(1)
    game = Game()
    game.run()
if __name__ == "__main__":
    main()