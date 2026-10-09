'''
main.py
Entry point for the Classic Snake game. Creates the tkinter root
window, instantiates the GUI, and starts the main loop.
'''
import tkinter as tk
from gui import GameGUI
def main():
    root = tk.Tk()
    GameGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()