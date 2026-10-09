'''
main.py
Entry point: bootstraps the Game and the Tkinter UI and starts the main loop.
'''
from game import Game
from ui import GameUI
def main():
    game = Game()
    ui = GameUI(game)
    ui.root.mainloop()
if __name__ == "__main__":
    main()