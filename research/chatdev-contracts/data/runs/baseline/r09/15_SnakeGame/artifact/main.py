'''
main.py
Entry point of the Classic Snake game.
Creates the Game instance and starts the main loop. Run this file with:
    python main.py
'''
from game import Game
def main():
    '''Boot the Snake game application.'''
    game = Game()
    game.run()
if __name__ == "__main__":
    main()