'''
main.py
Entry point for the Classic Sudoku game. Creates the Tk root window,
instantiates the GUI controller and starts the Tkinter event loop.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()