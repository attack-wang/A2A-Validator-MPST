'''
main.py
Entry point for the Reversi (Othello) application. Creates the root tkinter
window, instantiates the GUI and starts the tkinter event loop.
'''
import tkinter as tk
from gui import ReversiGUI
def main():
    root = tk.Tk()
    ReversiGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()