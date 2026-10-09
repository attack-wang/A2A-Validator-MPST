'''
main.py
Entry point for the Gomoku (Five in a Row) game.
Launches the Tkinter-based graphical interface. Run this file directly:
    python main.py
'''
import tkinter as tk
from gui import GomokuGUI
def main():
    """Create the application window and start the Tk event loop."""
    root = tk.Tk()
    GomokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()