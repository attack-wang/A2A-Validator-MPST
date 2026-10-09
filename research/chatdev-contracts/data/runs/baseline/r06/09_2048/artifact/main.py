'''
main.py
Entry point of the 2048 desktop application.
Wires together the game model (Game2048) and the pygame view (Renderer),
runs the main loop and translates keyboard events into game moves:
    * Arrow keys  -> slide/merge tiles (up/down/left/right)
    * R           -> start a new game
    * Escape / window close -> quit the application
'''
import sys
# Guarded dependency check: fail fast with a friendly message.
try:
    import pygame
except ImportError:
    sys.exit('pygame is required. Install it with: pip install pygame')
from game_logic import Game2048, UP, DOWN, LEFT, RIGHT
from renderer import Renderer
KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}
def process_events(game):
    '''
    Handle pygame events.
    Returns False when the application should quit, True otherwise.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r:
                game.reset()
                continue
            direction = KEY_TO_DIRECTION.get(event.key)
            if direction is not None and not game.is_game_over():
                game.move(direction)
    return True
def main():
    '''Create the game and renderer, then run the main loop.'''
    game = Game2048(size=4)
    renderer = Renderer(caption='2048')
    running = True
    while running:
        running = process_events(game)
        renderer.draw(game)
        renderer.tick(fps=60)
    renderer.quit()
    sys.exit(0)
if __name__ == '__main__':
    main()