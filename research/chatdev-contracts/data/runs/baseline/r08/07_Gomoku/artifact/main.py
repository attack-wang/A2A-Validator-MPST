'''
main.py
Entry point for the Gomoku game. Creates the Tkinter root window,
instantiates the Game controller and GomokuGUI view, centers the
window on the screen, and starts the Tkinter event loop.
'''
import tkinter as tk
from game import Game
from gui import GomokuGUI
def center_window(root):
    """Center the root window on the primary screen."""
    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"+{x}+{y}")
def main():
    """Build, center, and run the Gomoku application."""
    root = tk.Tk()
    game = Game()
    GomokuGUI(root, game)
    center_window(root)
    root.mainloop()
if __name__ == "__main__":
    main()