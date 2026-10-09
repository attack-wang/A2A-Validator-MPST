'''
main.py
Entry point for the Tic-Tac-Toe application.
Creates the main Tkinter window, instantiates the GUI controller,
and starts the event loop. Run this file to launch the game:
    python main.py
'''
import tkinter as tk
from gui import TicTacToeGUI
def main():
    """Create the application window and start the Tkinter event loop."""
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()