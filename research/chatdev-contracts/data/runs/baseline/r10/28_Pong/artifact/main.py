'''
main.py
Entry point for the two-player Pong game.
'''
import sys
def main():
    """Start the two-player Pong game."""
    try:
        from game import Game
    except ImportError as error:
        print("Could not start the game:", error)
        print("Make sure pygame is installed:  pip install pygame")
        sys.exit(1)
    pong = Game()
    pong.run()
if __name__ == "__main__":
    main()