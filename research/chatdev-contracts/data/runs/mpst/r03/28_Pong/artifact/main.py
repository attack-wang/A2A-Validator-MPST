'''
main.py
Entry point of the two-player Pong game.
Creates the Game instance and starts the main loop.
'''
from game import Game
def main():
    '''Create and run the Pong game.'''
    game = Game()
    game.run()
if __name__ == "__main__":
    main()