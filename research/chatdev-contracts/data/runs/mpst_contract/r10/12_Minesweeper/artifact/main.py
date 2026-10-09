import tkinter as tk

from gui import MinesweeperGUI


def main():
    root = tk.Tk()
    root.resizable(False, False)
    MinesweeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()