"""Entry point for the classic Minesweeper game."""
import tkinter as tk

from gui import MinesweeperGUI


def main():
    root = tk.Tk()
    MinesweeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()