'''
main.py
Entry point of the Gomoku application. It wires together the pure game logic
(Board), the match flow (GameController) and the Tkinter presentation layer
(GomokuGUI), then starts the desktop application.
'''
import tkinter as tk
from game_controller import GameController
from gui import GomokuGUI
def main():
    """Create the game window and launch the Gomoku application."""
    root = tk.Tk()
    controller = GameController()
    gui = GomokuGUI(root, controller)
    gui.run()
if __name__ == "__main__":
    main()