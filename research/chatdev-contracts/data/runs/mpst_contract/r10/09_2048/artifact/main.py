"""Entry point for the 2048 game."""
import tkinter as tk

from gui import GameGUI


def main():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()