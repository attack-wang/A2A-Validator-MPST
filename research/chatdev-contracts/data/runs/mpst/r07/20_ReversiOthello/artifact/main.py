'''
main.py
Entry point for the Reversi (Othello) application. It wires together the
Game controller and the tkinter-based GUI and launches the main loop.
'''
import tkinter as tk
from game import Game
from gui import ReversiGUI
def main():
    """Create the application window and start the game."""
    root = tk.Tk()
    game = Game()
    app = ReversiGUI(root, game)
    app.run()
if __name__ == "__main__":
    main()