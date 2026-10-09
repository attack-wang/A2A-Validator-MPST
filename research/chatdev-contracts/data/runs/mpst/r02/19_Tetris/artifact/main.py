'''
main.py
Entry point for the Tetris game.
Creates the Game instance and starts the main loop. Run this file with
`python main.py` (requires pygame: `pip install pygame`).
'''
from game import Game
def main():
    """Create and run the Tetris game."""
    Game().run()
if __name__ == '__main__':
    main()