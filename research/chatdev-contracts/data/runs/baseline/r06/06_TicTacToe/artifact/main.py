'''
main.py
Entry point for the Tic-Tac-Toe desktop application.
Creates the root tkinter window, attaches the TicTacToeGUI controller,
and starts the event loop. Run this file directly to play:
    python main.py
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    """Create the application window and start the GUI event loop."""
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()