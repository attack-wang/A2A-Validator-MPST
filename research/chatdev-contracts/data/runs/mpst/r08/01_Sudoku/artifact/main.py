'''
main.py
Entry point for the Sudoku puzzle game. Creates the root Tk window and
starts the application.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == '__main__':
    main()