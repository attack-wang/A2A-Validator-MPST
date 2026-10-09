'''
main.py
Entry point of the Snake game application. Creates the Game instance
and runs the main loop.
'''
from game import Game
def main():
    """Create and run the Snake game."""
    Game().run()
if __name__ == "__main__":
    main()