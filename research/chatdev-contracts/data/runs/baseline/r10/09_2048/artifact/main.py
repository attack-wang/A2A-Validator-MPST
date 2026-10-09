'''
Entry point for the 2048 game.
Initializes the game and renderer, then runs the main loop:
handles arrow-key input (plus WASD), updates game state, and renders
frames. Press R to restart and ESC to quit.
'''
import pygame
import sys
from game_logic import Game2048
from renderer import Renderer
def main():
    '''Run the 2048 game.'''
    game = Game2048(size=4)
    renderer = Renderer(size=4)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                direction = None
                if event.key in (pygame.K_UP, pygame.K_w):
                    direction = 'up'
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    direction = 'down'
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    direction = 'left'
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    direction = 'right'
                elif event.key == pygame.K_r:
                    # Restart the game
                    game = Game2048(size=4)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                if direction is not None:
                    game.move(direction)
        renderer.draw(game)
        clock.tick(60)
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()