'''
main.py
Entry point of the Reversi (Othello) console application.
Run this file to start a two-player hot-seat game:
    python main.py
'''
from game import Game
def main():
    """Create a Game instance and run it."""
    game = Game()
    game.run()
if __name__ == '__main__':
    main()