'''
main.py
Entry point of the Gomoku application.
Creates the Tkinter root window, wires together the game controller
(GomokuGame) and its graphical interface (GomokuGUI), and starts the
main event loop.
'''
import tkinter as tk
from game import GomokuGame
from gui import GomokuGUI
def main():
    """Initialize and run the Gomoku application."""
    root = tk.Tk()
    game = GomokuGame(board_size=15)
    GomokuGUI(root, game)
    root.mainloop()
if __name__ == "__main__":
    main()