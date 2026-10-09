'''
main.py
Entry point for the Reversi (Othello) console application.
Run this file to start an interactive two-player game:
    python main.py
'''
from game import Game
def main():
    '''Create a Game instance and run it until completion.'''
    game = Game()
    game.run()
if __name__ == "__main__":
    main()