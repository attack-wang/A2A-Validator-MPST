'''
main.py
Entry point of the Minesweeper application.
Creates the Tk root window, instantiates the GUI controller and
starts the Tkinter event loop.
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    """Create and run the Minesweeper application."""
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()