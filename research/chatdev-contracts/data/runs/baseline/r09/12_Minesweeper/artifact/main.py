'''
Entry point for the Minesweeper game.
Creates the main application window and starts the tkinter main loop.
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()