"""Entry point for the 2048 game."""
import tkinter as tk

from game import Game2048
from ui import GameUI


def main():
    root = tk.Tk()
    game = Game2048(size=4)
    GameUI(root, game)
    root.mainloop()


if __name__ == "__main__":
    main()