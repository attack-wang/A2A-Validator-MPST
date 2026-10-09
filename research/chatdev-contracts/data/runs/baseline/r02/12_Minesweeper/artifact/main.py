'''
Entry point for the Minesweeper game.
Creates the root tkinter window and starts the GUI application.
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()