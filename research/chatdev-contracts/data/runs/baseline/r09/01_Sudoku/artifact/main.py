'''
main.py — Entry point for the classic 9x9 Sudoku game.
Creates the Tk root window, attaches the SudokuGUI controller and
starts the Tkinter event loop. Run this file directly to play:
    python main.py
'''
import tkinter as tk
from game_gui import SudokuGUI
def main():
    """Build the main window, attach the GUI and enter the event loop."""
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()