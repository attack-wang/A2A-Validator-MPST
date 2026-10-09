'''
main.py
Entry point of the Tic-Tac-Toe application.
Creates the root tkinter window, instantiates the TicTacToeGame
controller (which builds the whole user interface), and hands control
over to the tkinter event loop until the user closes the game.
Run with:  python main.py
'''
import tkinter as tk
from game import TicTacToeGame
def main():
    """Create the application window and start the tkinter event loop."""
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
if __name__ == "__main__":
    main()