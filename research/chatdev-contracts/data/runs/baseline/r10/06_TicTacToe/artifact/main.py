'''
main.py
Entry point for the Tic-Tac-Toe application. Creates the root tkinter
window, instantiates the GUI controller, and starts the event loop.
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    '''Build the application window and run the Tk event loop.'''
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()