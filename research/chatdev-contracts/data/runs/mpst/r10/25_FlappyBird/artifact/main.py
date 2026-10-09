'''
main.py
Entry point for the Flappy Bird clone. Boots the Game object and
handles a clean shutdown.
'''
import pygame
from game import Game
def main():
    """Create the Game, run its loop, and guarantee pygame shuts down."""
    game = Game()
    try:
        game.run()
    finally:
        pygame.quit()
if __name__ == "__main__":
    main()