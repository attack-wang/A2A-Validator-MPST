'''
main.py
Entry point for the Minesweeper application.
'''
import tkinter as tk
from gui import GameGUI
def main():
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()