'''
main.py
Entry point of the Connect Four application. It builds a Game instance
and starts the interactive, two-player console match.
'''
from game import Game
def main() -> None:
    """Create a new Connect Four game and run it until completion."""
    game = Game()
    game.play()
if __name__ == '__main__':
    main()