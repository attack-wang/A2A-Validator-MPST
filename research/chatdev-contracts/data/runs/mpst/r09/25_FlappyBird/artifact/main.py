'''
Entry point: initializes pygame and starts the game loop.
'''
import sys
try:
    import pygame
except ImportError:
    print("The 'pygame' module is required but not installed.")
    print("Install it with:  pip install pygame")
    sys.exit(1)
import settings
from game import Game
def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.run()
    pygame.quit()
if __name__ == "__main__":
    main()