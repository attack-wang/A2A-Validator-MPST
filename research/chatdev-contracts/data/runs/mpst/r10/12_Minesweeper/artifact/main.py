'''
main.py
Entry point for the Minesweeper game.
Creates the Tk root window, instantiates the GUI from gui.py and starts
the Tk event loop. Run this file to play:  python main.py
'''
import tkinter as tk
from gui import MinesweeperGUI
def main():
    '''Create the Tk root window and start the application.'''
    root = tk.Tk()
    MinesweeperGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()