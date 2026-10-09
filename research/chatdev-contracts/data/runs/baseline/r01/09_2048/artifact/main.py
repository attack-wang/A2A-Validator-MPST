'''
Entry point for the 2048 game: initializes pygame, creates the Game and
Renderer, and runs the main loop with keyboard event handling.
'''
import sys
try:
    import pygame
except ImportError:
    sys.exit('pygame is required. Install it with: pip install pygame')
from config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from game import Game
from renderer import Renderer
def main():
    '''Initialize pygame, run the game loop, and clean up on exit.'''
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()
    game = Game()          # board, score, spawn logic
    renderer = Renderer(window)
    running = True
    while running:
        # ---------------- Event handling ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    game.move('left')
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    game.move('right')
                elif event.key in (pygame.K_UP, pygame.K_w):
                    game.move('up')
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    game.move('down')
                elif event.key == pygame.K_r:      # restart anytime
                    game.reset()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        # ---------------- Rendering ----------------
        renderer.draw(game)
        pygame.display.flip()
        # ---------------- Frame-rate control ----------------
        clock.tick(FPS)
    pygame.quit()
    sys.exit(0)
if __name__ == '__main__':
    main()