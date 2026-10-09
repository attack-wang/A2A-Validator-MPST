'''
main.py
Entry point for the Reversi (Othello) game.
Creates the Tk root window, attaches the ReversiGUI and starts the
Tkinter event loop.
'''
import tkinter as tk
from gui import ReversiGUI
def main():
    '''Launch the Reversi game window and enter the main event loop.'''
    root = tk.Tk()
    ReversiGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()