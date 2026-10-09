'''
Entry point for the Minesweeper game.
'''
import tkinter as tk
from gui import MinesweeperGUI
from game import Game
def main():
    root = tk.Tk()
    game = Game()
    gui = MinesweeperGUI(root, game)
    gui.run()
if __name__ == "__main__":
    main()