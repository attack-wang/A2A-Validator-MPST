'''
main.py
Entry point for the Connect Four application. Creates a Game instance
and starts the interactive match between two players.
'''
from game import Game
def main():
    """Instantiate and run the Connect Four game."""
    game = Game()
    game.play()
if __name__ == "__main__":
    main()