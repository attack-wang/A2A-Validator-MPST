'''
main.py
Entry point for the Classic Snake game. Creates the Game instance
and starts the main loop.
'''
from game import Game
def main():
    """Create and run the Snake game."""
    game = Game()
    game.run()
if __name__ == "__main__":
    main()