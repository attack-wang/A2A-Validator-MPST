'''
main.py
Entry point for the Minesweeper application.
'''
import tkinter as tk
from game import Game
def main():
    root = tk.Tk()
    root.title("Minesweeper - ChatDev")
    root.resizable(False, False)
    Game(root)
    root.mainloop()
if __name__ == "__main__":
    main()