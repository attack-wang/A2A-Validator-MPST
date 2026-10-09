'''
main.py
Entry point of the 2048 game. Wires together the game logic and the
pygame renderer and runs the main event loop:
  - Arrow keys (or WASD) slide the tiles.
  - R restarts the game at any time.
  - Closing the window quits the application.
'''
import sys
try:
    import pygame
except ImportError:
    print("pygame is required to run this game. Install it with:\n"
          "    pip install pygame")
    sys.exit(1)
import config as cfg
from game_logic import Game2048, UP, DOWN, LEFT, RIGHT
from renderer import Renderer
# Map keyboard keys to game directions.
KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_down: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}
def handle_keydown(event, game):
    '''Translate a KEYDOWN event into a game action (move or restart).'''
    if event.key == pygame.K_r:
        game.reset()
        return
    if game.game_over:
        return  # Ignore movement keys once no moves are possible
    direction = KEY_TO_DIRECTION.get(event.key)
    if direction is not None:
        game.move(direction)
def main():
    '''Initialize the game and run the main loop until the user quits.'''
    renderer = Renderer(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT, cfg.WINDOW_CAPTION)
    game = Game2048(cfg.GRID_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, game)
        renderer.draw(game)
        renderer.clock.tick(cfg.FPS)
    pygame.quit()
    sys.exit(0)
if __name__ == "__main__":
    main()