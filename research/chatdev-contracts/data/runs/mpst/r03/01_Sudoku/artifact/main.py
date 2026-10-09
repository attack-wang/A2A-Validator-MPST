'''
Main entry point for the Sudoku application.
Launches the GUI and starts the game loop.
'''
import tkinter as tk
from gui import SudokuGUI
def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()