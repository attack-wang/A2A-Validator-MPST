'''
main.py
Entry point for the 2048 game.
Run this file to start the game:  python main.py
'''
import tkinter as tk
from gui import Game2048GUI
def main():
    root = tk.Tk()
    Game2048GUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()