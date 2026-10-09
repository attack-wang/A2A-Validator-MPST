'''
Entry point for the Classic Snake game.
'''
import tkinter as tk
from game import Game
def main():
    '''Create the application window and start the game.'''
    root = tk.Tk()
    Game(root)
    root.mainloop()
if __name__ == "__main__":
    main()