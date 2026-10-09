'''
main.py
Entry point of the Tetris game.
Creates the Game instance and starts the main loop. pygame is imported
inside a try/except block so that a missing installation produces a clear,
friendly hint ("pip install pygame") instead of a raw ModuleNotFoundError
traceback. The __main__ guard guarantees the game actually starts when
this file is executed directly.
'''
import sys
try:
    import pygame
except ImportError:
    print("Error: the 'pygame' module is required to play Tetris.")
    print("Install it by running:  pip install pygame")
    sys.exit(1)
from game import Game
def main():
    """Create the game and run its main loop until the window is closed."""
    game = Game()
    game.run()
    pygame.quit()
if __name__ == '__main__':
    main()