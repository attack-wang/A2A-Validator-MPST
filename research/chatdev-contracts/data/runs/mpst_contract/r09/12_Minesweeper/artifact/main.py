"""Entry point for the classic Minesweeper game."""
import tkinter as tk

from ui import MinesweeperUI


def main():
    root = tk.Tk()
    MinesweeperUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()