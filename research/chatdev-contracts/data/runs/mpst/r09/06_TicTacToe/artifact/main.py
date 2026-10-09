'''
main.py
Entry point of the tic-tac-toe application. It opens the main window,
optionally asks for the two players' names, wires the Game model to the
Tkinter interface, and starts the event loop.
'''
import tkinter as tk
from tkinter import simpledialog
from game import Game
from gui import TicTacToeGUI
def _clean(name, default):
    """
    Normalize a player name: strip whitespace and fall back to a default
    when the input is empty or the dialog was cancelled.
    Args:
        name (str | None): raw user input.
        default (str): fallback name.
    Returns:
        str: a non-empty, trimmed player name.
    """
    name = (name or "").strip()
    return name if name else default
def ask_player_names(root):
    """
    Prompt for both players' names, falling back to defaults on cancel.
    Args:
        root (tk.Tk): parent window for the dialogs.
    Returns:
        tuple[str, str]: names for player X and player O.
    """
    name_x = simpledialog.askstring(
        "Players", "Name of Player 1 (plays X):",
        initialvalue="Player 1", parent=root,
    )
    name_o = simpledialog.askstring(
        "Players", "Name of Player 2 (plays O):",
        initialvalue="Player 2", parent=root,
    )
    return _clean(name_x, "Player 1"), _clean(name_o, "Player 2")
def main():
    """Launch the tic-tac-toe game."""
    root = tk.Tk()
    root.withdraw()  # hide the empty main window while asking for names
    name_x, name_o = ask_player_names(root)
    game = Game(name_x, name_o)
    root.deiconify()
    TicTacToeGUI(root, game)
    root.mainloop()
if __name__ == "__main__":
    main()