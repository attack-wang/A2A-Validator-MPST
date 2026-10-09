'''
main.py
Entry point for the Tic-Tac-Toe application.
Creates the root tkinter window, instantiates the GUI, and starts the event loop.
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    '''Create the main window, launch the GUI, and start the tkinter event loop.'''
    root = tk.Tk()
    app = TicTacToeGUI(root)
    app.run()
if __name__ == '__main__':
    main()