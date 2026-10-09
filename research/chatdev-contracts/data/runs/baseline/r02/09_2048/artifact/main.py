'''
main.py
Entry point for the 2048 game. Initializes pygame, creates the game state
and renderer, and runs the main loop: polling keyboard events (arrow keys /
WASD to move, R to restart, ESC to quit), updating game logic, and drawing.
'''
import pygame
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game_logic import Game2048
from renderer import Renderer
def main():
    """Set up the window and run the 2048 game loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    game = Game2048()
    renderer = Renderer(screen)
    # Map keyboard keys to movement directions
    direction_map = {
        pygame.K_LEFT: 'left',
        pygame.K_a: 'left',
        pygame.K_RIGHT: 'right',
        pygame.K_d: 'right',
        pygame.K_UP: 'up',
        pygame.K_w: 'up',
        pygame.K_DOWN: 'down',
        pygame.K_s: 'down',
    }
    running = True
    while running:
        # ------------------------------------------------------------------
        # Event handling
        # ------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key in direction_map and not game.game_over:
                    game.move(direction_map[event.key])
        # ------------------------------------------------------------------
        # Render current state
        # ------------------------------------------------------------------
        renderer.draw(game)
        clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    main()