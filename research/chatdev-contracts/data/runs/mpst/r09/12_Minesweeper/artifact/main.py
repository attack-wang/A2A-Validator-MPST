'''
Entry point for the Minesweeper game.
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    root = tk.Tk()
    gui = MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()