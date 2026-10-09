'''
Entry point for the 2048 game.
Sets up the pygame window, maps keyboard input (arrow keys and WASD)
to movement directions, routes R to a game restart, and runs the main
render loop until the user closes the window.
'''
import sys
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game2048
from renderer import Renderer
# Map keyboard keys to movement directions (arrow keys plus WASD).
DIRECTION_KEYS = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
    pygame.K_w: 'up',
    pygame.K_s: 'down',
    pygame.K_a: 'left',
    pygame.K_d: 'right',
}
def process_events(game):
    '''
    Process the pygame event queue.
    Returns False when the user closes the window, True otherwise.
    Movement keys trigger game moves; R restarts the game.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            direction = DIRECTION_KEYS.get(event.key)
            if direction:
                game.move(direction)
            elif event.key == pygame.K_r:
                game.reset()
    return True
def main():
    '''Set up pygame and run the game loop until the window is closed.'''
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()
    game = Game2048()
    renderer = Renderer(window)
    running = True
    while running:
        running = process_events(game)
        renderer.draw(game)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()