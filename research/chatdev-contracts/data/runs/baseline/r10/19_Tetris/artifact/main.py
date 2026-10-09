'''
main.py
Entry point for the Tetris game: creates the Game instance and starts the main loop.
'''
from game import Game
def main():
    """Instantiate and run the Tetris game."""
    Game().run()
if __name__ == "__main__":
    main()