'''
main.py
Entry point for the Classic Sudoku application.
Creates the root Tk window, instantiates the SudokuGUI controller and
starts the tkinter event loop.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()