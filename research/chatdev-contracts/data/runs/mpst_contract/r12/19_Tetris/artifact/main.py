import tkinter as tk

from tetris import Tetris


def main():
    root = tk.Tk()
    root.title('Tetris')
    Tetris(root)
    root.mainloop()


if __name__ == '__main__':
    main()