'''
main.py
Entry point for the Tic-Tac-Toe application.
Creates the root Tkinter window, centers it on the primary screen,
attaches the TicTacToeGUI front-end, and starts the Tkinter main event
loop so the game can be launched directly with `python main.py`.
'''
import tkinter as tk
from gui import TicTacToeGUI
def _center_window(window, width=420, height=560):
    """
    Center the given window on the primary screen.
    Args:
        window (tk.Tk): The window to position.
        width (int): Desired window width in pixels.
        height (int): Desired window height in pixels.
    """
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
def main():
    """Build and run the Tic-Tac-Toe application."""
    root = tk.Tk()
    _center_window(root)
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()