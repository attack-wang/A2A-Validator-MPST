'''
main.py
Entry point of the Gomoku (Five-in-a-Row) application.
Creates the Tk root window, instantiates the game logic (`Board`) and the
graphical front-end (`GomokuGUI`) and starts the Tkinter event loop.
Run with:  python main.py
'''
import tkinter as tk
from board import Board
from gui import GomokuGUI
def main():
    '''Build the application and enter the GUI event loop.'''
    root = tk.Tk()
    board = Board()
    GomokuGUI(root, board)
    root.mainloop()
if __name__ == "__main__":
    main()