'''
main.py
Entry point for the Tetris game. Creates the Game instance and starts the loop.
'''
from game import Game
def main():
    game = Game()
    game.run()
if __name__ == "__main__":
    main()