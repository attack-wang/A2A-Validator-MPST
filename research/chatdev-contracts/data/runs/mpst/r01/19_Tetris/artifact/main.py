'''
Entry point: game loop, keyboard input with DAS auto-repeat, pause/restart.
'''
import pygame
import sys
from constants import FPS, DAS_DELAY, DAS_REPEAT
from game import Game
from renderer import Renderer
def main():
    """Run the Tetris application until the window is closed."""
    pygame.init()
    renderer = Renderer()
    clock = pygame.time.Clock()
    game = Game()
    held = {}        # key -> seconds the key has been held (for DAS repeat)
    paused = False
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # frame time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and not game.game_over:
                    paused = not paused                      # toggle pause
                elif event.key == pygame.K_r:
                    game, paused, held = Game(), False, {}   # restart
                elif not paused and not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0); held[pygame.K_LEFT] = 0.0
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0); held[pygame.K_RIGHT] = 0.0
                    elif event.key == pygame.K_DOWN:
                        game.soft_drop(); held[pygame.K_DOWN] = 0.0
                    elif event.key == pygame.K_UP:
                        game.rotate()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
            elif event.type == pygame.KEYUP:
                held.pop(event.key, None)                    # stop auto-repeat
        if not paused and not game.game_over:
            # DAS: after DAS_DELAY, repeat the held action every DAS_REPEAT
            for key in list(held.keys()):
                held[key] += dt
                if held[key] >= DAS_DELAY:
                    if key == pygame.K_LEFT: game.move(-1, 0)
                    elif key == pygame.K_RIGHT: game.move(1, 0)
                    elif key == pygame.K_DOWN: game.soft_drop()
                    held[key] = DAS_DELAY - DAS_REPEAT
            game.update(dt)                                  # gravity + auto-lock
        renderer.draw(game, paused)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()