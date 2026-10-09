'''
main.py
Entry point for the Gomoku game application.
'''
import tkinter as tk
from gui import GomokuGUI
def main():
    """Create the main window and start the Gomoku game."""
    root = tk.Tk()
    GomokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()