'''
main.py
Entry point of the 2048 game. It wires together the game logic and the
renderer, handles keyboard input (arrow keys to move, R to restart,
Esc/Q to quit), and runs the main game loop.
'''
import sys
import pygame
from game_logic import Game2048
from renderer import Renderer
DIRECTION_BY_KEY = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
}
def main():
    '''Initialize the game and run the main loop until the user quits.'''
    renderer = Renderer()
    game = Game2048()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in DIRECTION_BY_KEY:
                    game.move(DIRECTION_BY_KEY[event.key])
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
        renderer.draw(game)
    pygame.quit()
    sys.exit(0)
if __name__ == '__main__':
    main()