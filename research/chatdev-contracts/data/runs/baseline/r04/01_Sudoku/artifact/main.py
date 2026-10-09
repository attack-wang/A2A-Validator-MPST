'''
main.py
Entry point for the Sudoku puzzle game. Creates the root Tk window
and starts the SudokuGUI application.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    """Create the root window and run the application."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()