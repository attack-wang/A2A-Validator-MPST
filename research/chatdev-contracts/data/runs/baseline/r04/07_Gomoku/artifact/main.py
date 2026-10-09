'''
Entry point for the Gomoku game.
Launches the pygame application; gives a friendly hint if pygame
is missing instead of crashing with a raw traceback.
'''
import sys
def main():
    """Create and run the Gomoku game."""
    try:
        from game import Game
    except ImportError as exc:
        print("Failed to import required modules: {}".format(exc))
        if "pygame" in str(exc):
            print("Please install pygame with: pip install pygame")
        sys.exit(1)
    game = Game()
    game.run()
if __name__ == "__main__":
    main()