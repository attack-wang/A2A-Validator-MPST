'''
Entry point for the ChatDev Crossword Puzzle console application.
Imports the CrosswordGame class from game.py and starts the
interactive game loop when this file is executed directly.
'''
from game import CrosswordGame
def main():
    """Create the game and start the interactive loop."""
    CrosswordGame().run()
if __name__ == "__main__":
    main()