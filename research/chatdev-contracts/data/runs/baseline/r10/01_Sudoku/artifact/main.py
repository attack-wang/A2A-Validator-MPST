'''
main.py — entry point for the Sudoku application.
Launches the Tkinter main window and starts the SudokuGUI application.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == '__main__':
    main()