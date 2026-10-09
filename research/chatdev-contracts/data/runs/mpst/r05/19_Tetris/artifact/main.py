'''
main.py
Entry point: initializes pygame, creates the Game and Renderer, and runs the
main loop with keyboard handling (move, rotate, soft/hard drop, restart)
and per-frame rendering. Gracefully reports a missing pygame installation.
'''
import sys
try:
    import pygame
except ImportError:
    sys.exit("pygame is not installed. Install it with: pip install pygame")
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, DAS_DELAY, DAS_RATE
from game import Game
from renderer import Renderer
def handle_held_keys(game, keys, timers, dt):
    """Apply auto-repeat movement for held left/right/down keys."""
    actions = [
        (pygame.K_LEFT, 'left', game.move_left),
        (pygame.K_RIGHT, 'right', game.move_right),
        (pygame.K_DOWN, 'down', game.move_down),
    ]
    for key, name, action in actions:
        if keys[key]:
            timers[name] += dt
            if timers[name] >= DAS_DELAY:
                action()
                timers[name] = DAS_DELAY - DAS_RATE  # subsequent repeats every DAS_RATE
        else:
            timers[name] = 0.0
def handle_events(game, timers):
    """Process one-shot key presses: rotation, hard drop, restart, quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            elif event.key == pygame.K_SPACE:
                game.hard_drop()
            elif event.key == pygame.K_LEFT:
                game.move_left()
                timers['left'] = 0.0  # restart DAS delay after the initial press
            elif event.key == pygame.K_RIGHT:
                game.move_right()
                timers['right'] = 0.0
            elif event.key == pygame.K_DOWN:
                game.move_down()
                timers['down'] = 0.0
            elif event.key == pygame.K_r and game.game_over:
                game.restart()
def main():
    """Initialize pygame and run the main game loop."""
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(window)
    timers = {'left': 0.0, 'right': 0.0, 'down': 0.0}
    while True:
        dt = clock.tick(FPS) / 1000.0  # seconds since last frame
        handle_events(game, timers)
        keys = pygame.key.get_pressed()
        handle_held_keys(game, keys, timers, dt)
        game.update(dt)
        renderer.draw(game)
if __name__ == '__main__':
    main()