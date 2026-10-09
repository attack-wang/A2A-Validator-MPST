'''
main.py
Entry point for the Tic-Tac-Toe application. Creates the root Tk window,
attaches the GUI built in gui.py, and starts the Tkinter main event loop.
Run this file directly to launch the game: python main.py
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    """
    Create the main application window, attach the Tic-Tac-Toe GUI,
    and start the Tkinter event loop.
    """
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()