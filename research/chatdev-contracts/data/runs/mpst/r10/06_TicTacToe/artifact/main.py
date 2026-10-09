'''
Main entry point for the Tic-Tac-Toe game application.
Running this module launches the two-player Tic-Tac-Toe game with a
user-friendly graphical interface: a standard 3x3 grid where players
alternately place X and O marks by clicking cells, with automatic
winner detection, draw detection, move tracking, a scoreboard and a
"Play Again" option.
'''
from gui import TicTacToeGUI
def main():
    """Create the game window and start the application event loop."""
    app = TicTacToeGUI()
    app.run()
if __name__ == "__main__":
    main()