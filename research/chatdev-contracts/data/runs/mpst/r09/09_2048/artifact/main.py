'''
main.py
Entry point for the 2048 game. Creates the game logic and the Tkinter UI
and starts the application main loop.
'''
import tkinter as tk
from game_logic import Game2048
from ui import GameUI
def main():
    root = tk.Tk()
    game = Game2048(size=4)
    ui = GameUI(root, game)
    root.mainloop()
if __name__ == '__main__':
    main()