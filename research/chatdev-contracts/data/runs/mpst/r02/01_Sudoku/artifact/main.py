'''
main.py — entry point for the Sudoku game.
Creates the Tk root window, instantiates the SudokuGUI from gui.py
(the single module that defines the SudokuGUI class) and starts the
main event loop.
'''
import tkinter as tk
from gui import SudokuGUI
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()