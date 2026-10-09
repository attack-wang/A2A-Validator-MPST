'''
main.py
Entry point for the tic-tac-toe application. Initializes the tkinter root
window, builds the game GUI, and starts the main event loop.
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    '''Create the application window and launch the game.'''
    root = tk.Tk()
    app = TicTacToeGUI(root)
    app.run()
if __name__ == "__main__":
    main()