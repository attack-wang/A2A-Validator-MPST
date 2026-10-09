'''
main.py
Entry point for the Gomoku application. Wires together the game
controller and the tkinter GUI and starts the main event loop.
'''
import tkinter as tk
from game import Game
from gui import GomokuGUI
def main():
    """Create the application window and run the Gomoku game."""
    root = tk.Tk()
    game = Game()
    GomokuGUI(root, game)
    root.mainloop()
if __name__ == "__main__":
    main()