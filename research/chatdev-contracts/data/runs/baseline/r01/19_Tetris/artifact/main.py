'''
main.py
Entry point for the Tetris game: creates the Game instance and starts
the main loop. Run with:  python main.py
'''
from game import Game
def main():
    """Create and run the Tetris game."""
    Game().run()
if __name__ == "__main__":
    main()