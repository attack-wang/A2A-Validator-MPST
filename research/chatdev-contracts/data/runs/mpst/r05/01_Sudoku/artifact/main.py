'''
main.py
Entry point of the Sudoku application.
Creates the Tk root window, instantiates the SudokuGUI controller
and starts the Tk event loop so the player can interact with the game.
'''
import tkinter as tk
from gui import SudokuGUI
def main():
    """Launch the Sudoku game window."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()