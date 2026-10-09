'''
main.py
Entry point for the Reversi (Othello) console game.
Run this file to start a new two-player game:
    python main.py
'''
from game import Game
def main():
    '''Create and run a new Reversi game.'''
    game = Game()
    game.run()
if __name__ == '__main__':
    main()