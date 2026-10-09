'''
main.py
Entry point for the Sudoku puzzle game. Creates the game controller and
starts the application loop.
'''
from game_controller import GameController
def main():
    """Create the game controller and launch the Sudoku application."""
    controller = GameController()
    controller.run()
if __name__ == "__main__":
    main()