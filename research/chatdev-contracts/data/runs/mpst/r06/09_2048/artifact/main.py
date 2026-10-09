'''
main.py
Entry point for the 2048 game. Creates the Tkinter root window,
instantiates the game model and the GUI, and starts the main loop.
'''
import tkinter as tk
from ui import GameUI
def main():
    root = tk.Tk()
    GameUI(root)
    root.mainloop()
if __name__ == '__main__':
    main()