'''
Main entry point: creates the game state and launches the graphical interface.
'''
import sys
from game import Game
def main():
    '''Create the game state and launch the graphical interface.'''
    try:
        from gui import ReversiGUI
    except ImportError:
        print("Pygame is required to run this game. Install it with: pip install pygame")
        sys.exit(1)
    game = Game()
    gui = ReversiGUI(game)
    gui.run()
if __name__ == "__main__":
    main()