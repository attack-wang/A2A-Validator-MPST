'''main.py: Entry point...'''
from game import Game
from ui import UI
def main():
    game = Game()
    ui = UI(game)
    ui.run()
if __name__ == "__main__":
    main()