'''Entry point for the Space Invaders game.'''
from game import Game
def main():
    '''Create the game and start the main loop.'''
    game = Game()
    game.run()
if __name__ == "__main__":
    main()