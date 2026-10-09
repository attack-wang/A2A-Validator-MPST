'''
main.py
Entry point for the classic Sudoku puzzle game.
Creates the application window, wires the SudokuGUI to the root Tk window,
and starts the Tkinter main event loop.
'''
import tkinter as tk
from sudoku_gui import SudokuGUI
def main():
    """Create the main window, attach the game UI, and run the event loop."""
    root = tk.Tk()
    root.title("Classic Sudoku")
    root.resizable(False, False)
    gui = SudokuGUI(root)
    gui.pack(fill="both", expand=True)
    root.mainloop()
if __name__ == "__main__":
    main()