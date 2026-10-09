'''
Main entry point for the Minesweeper game.
Run this file to launch the Tkinter window:
    python main.py
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    """Create the root window and start the Tkinter event loop."""
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()