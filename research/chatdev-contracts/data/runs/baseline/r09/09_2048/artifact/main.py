'''
Entry point for the 2048 game.
Creates the Tkinter root window, instantiates the game model and its GUI,
then starts the main event loop.
'''
import tkinter as tk
from constants import GRID_SIZE
from game_logic import Game2048
from gui import Game2048GUI
def main():
    root = tk.Tk()
    game = Game2048(size=GRID_SIZE)
    gui = Game2048GUI(root, game)
    root.mainloop()
if __name__ == "__main__":
    main()