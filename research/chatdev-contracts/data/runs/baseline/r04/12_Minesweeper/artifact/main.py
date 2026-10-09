'''
main.py
Entry point of the Minesweeper application.
Creates the Tk root window, instantiates the MinesweeperGUI controller and
starts the Tkinter event loop.
'''
import tkinter as tk
from minesweeper_gui import MinesweeperGUI
def main():
    """Build the main window and run the application."""
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()