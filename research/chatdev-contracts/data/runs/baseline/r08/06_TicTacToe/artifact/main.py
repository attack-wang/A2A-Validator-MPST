'''
main.py
Entry point for the Tic-Tac-Toe game. Creates the GUI and starts
the main game loop.
'''
import sys
from gui import GameGUI
def main():
    '''Launch the Tic-Tac-Toe game and handle fatal errors gracefully.'''
    try:
        game = GameGUI()
        game.run()
    except Exception as exc:
        print("Fatal error while running the game: {}".format(exc))
        sys.exit(1)
if __name__ == "__main__":
    main()