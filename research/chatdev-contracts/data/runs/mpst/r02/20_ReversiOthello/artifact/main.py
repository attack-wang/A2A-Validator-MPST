'''
main.py
Entry point for the Reversi (Othello) game. Creates the application
window and starts the tkinter event loop.
'''
import tkinter as tk
from gui import ReversiGUI
def main():
    root = tk.Tk()
    app = ReversiGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()