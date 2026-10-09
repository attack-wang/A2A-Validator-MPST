'''
main.py
Entry point for the Classic Snake game. Creates the Game instance
and starts the main loop.
'''
from game import Game
def main():
    """Instantiate and run the Snake game."""
    Game().run()
if __name__ == "__main__":
    main()