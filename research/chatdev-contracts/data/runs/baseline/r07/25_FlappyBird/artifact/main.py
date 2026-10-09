'''
Main entry point for the Flappy Bird clone.
Verifies that the pygame dependency is available before importing the game
modules and prints clear installation instructions when it is missing,
instead of crashing with an unhandled ModuleNotFoundError.
'''
import sys
def _ensure_pygame():
    """Exit gracefully with install instructions if pygame is missing."""
    try:
        import pygame  # noqa: F401  (imported only to check availability)
    except ImportError:
        print("=" * 62)
        print(" ERROR: The 'pygame' module is required but not installed.")
        print(" Install it with one of the following commands:")
        print("     pip install pygame")
        print("     pip install -r requirements.txt")
        print("=" * 62)
        sys.exit(1)
def main():
    """Create and run the Flappy Bird game."""
    _ensure_pygame()
    from game import Game  # imported after the dependency check
    game = Game()
    game.run()
if __name__ == "__main__":
    main()