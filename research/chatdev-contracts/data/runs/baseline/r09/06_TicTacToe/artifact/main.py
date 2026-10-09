'''
main.py
Entry point for the tic-tac-toe application.
Creates the root tkinter window, wires the game logic (TicTacToeGame) to
the graphical interface (TicTacToeGUI), and starts the main event loop.
'''
import tkinter as tk
from game_logic import TicTacToeGame
from gui import TicTacToeGUI
def main():
    """Launch the tic-tac-toe game."""
    root = tk.Tk()
    game = TicTacToeGame()
    TicTacToeGUI(root, game)
    root.mainloop()
if __name__ == '__main__':
    main()