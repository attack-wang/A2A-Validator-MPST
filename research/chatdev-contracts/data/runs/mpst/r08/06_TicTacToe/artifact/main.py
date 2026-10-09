'''
main.py
Entry point for the tic-tac-toe application.
Prompts both players for their names, then launches the GUI.
'''
import tkinter as tk
from tkinter import simpledialog
from gui import TicTacToeGUI
def main():
    """Create the root window, collect player names, and start the game."""
    root = tk.Tk()
    root.withdraw()  # Hide the empty root window during setup dialogs
    name_x = simpledialog.askstring(
        "Player Setup",
        "Enter name for Player 1 (X):",
        initialvalue="Player 1",
        parent=root,
    ) or "Player 1"
    name_o = simpledialog.askstring(
        "Player Setup",
        "Enter name for Player 2 (O):",
        initialvalue="Player 2",
        parent=root,
    ) or "Player 2"
    root.deiconify()  # Show the window again for the game
    app = TicTacToeGUI(root, player_x_name=name_x, player_o_name=name_o)
    app.run()
if __name__ == "__main__":
    main()