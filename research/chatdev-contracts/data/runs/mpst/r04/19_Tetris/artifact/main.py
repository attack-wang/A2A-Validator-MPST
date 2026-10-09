'''
Entry point for the Tetris game.
Creates the Game instance and starts the main loop.
'''
from game import Game
if __name__ == "__main__":
    game = Game()
    game.run()