'''
main.py
Entry point of the Tic-Tac-Toe desktop application.
Creates the root tkinter window, builds the TicTacToeGUI on top of it
and starts the tkinter event loop so the two players can start playing.
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    """Launch the Tic-Tac-Toe game window and run the event loop."""
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()