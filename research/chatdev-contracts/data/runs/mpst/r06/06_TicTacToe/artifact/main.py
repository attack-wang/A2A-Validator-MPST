'''
main.py
Entry point for the Tic-Tac-Toe application. Creates the root tkinter
window, instantiates the GUI controller, and starts the tkinter event
loop so players can begin playing immediately.
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    """Create the application window and launch the Tic-Tac-Toe game."""
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()