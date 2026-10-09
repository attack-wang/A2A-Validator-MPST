'''
main.py
Entry point for the tic-tac-toe application.
Creates the main Tkinter window, embeds the game UI,
and starts the event loop.
'''
import tkinter as tk
from tictactoeui import TicTacToeUI
def main():
    """Build the application window and run the Tk event loop."""
    root = tk.Tk()
    TicTacToeUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()