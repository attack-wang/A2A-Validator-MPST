import tkinter as tk

from pong import Game


def main():
    root = tk.Tk()
    root.title("Pong - Two Player")
    root.resizable(False, False)
    game = Game(root)
    root.protocol("WM_DELETE_WINDOW", game.quit)
    root.mainloop()


if __name__ == "__main__":
    main()