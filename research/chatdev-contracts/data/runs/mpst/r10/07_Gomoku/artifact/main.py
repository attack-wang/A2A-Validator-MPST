'''
main.py
Entry point for the Gomoku application.
Creates the game controller and launches the graphical interface.
'''
from game import Game
from gui import GomokuGUI
def main():
    """Create a new 15x15 Gomoku game and start the GUI event loop."""
    game = Game(board_size=15)
    gui = GomokuGUI(game)
    gui.run()
if __name__ == "__main__":
    main()