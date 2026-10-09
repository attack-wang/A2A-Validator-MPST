'''
main.py
Entry point for the classic Sudoku puzzle game.
Run this file to launch the game:
    python main.py
'''
from game_controller import GameController
def main():
    """Create the game controller and start the application."""
    game = GameController()
    game.run()
if __name__ == "__main__":
    main()