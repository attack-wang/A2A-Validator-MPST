'''
main.py — entry point: builds the Tk root window and starts the Minesweeper GUI.
'''
import tkinter as tk
from game_logic import Difficulty
from gui import MinesweeperGUI
def main():
    """Create the application window and run the Tk event loop."""
    root = tk.Tk()
    MinesweeperGUI(root, Difficulty.BEGINNER)
    root.mainloop()
if __name__ == "__main__":
    main()