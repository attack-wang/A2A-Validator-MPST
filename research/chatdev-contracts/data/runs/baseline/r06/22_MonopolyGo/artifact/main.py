'''
main.py
Entry point for the simplified Monopoly Go! game.
'''
import ui
from game import Game
def main():
    ui.banner("Welcome to Simplified Monopoly Go!")
    names = ui.prompt_player_names(default_count=2)
    game = Game(names)
    game.play()
if __name__ == '__main__':
    main()