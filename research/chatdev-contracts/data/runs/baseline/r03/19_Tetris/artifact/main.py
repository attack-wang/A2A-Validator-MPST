'''
main.py
Entry point: initializes pygame, creates the window, runs the game loop and
handles all input (including key-repeat for held movement keys).
'''
import pygame
from constants import (FPS, WINDOW_WIDTH, WINDOW_HEIGHT,
                       KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
from game import Game
from renderer import Renderer
class InputRepeater:
    """Tracks held keys and emits repeated events after an initial delay."""
    def __init__(self, delay=KEY_REPEAT_DELAY, interval=KEY_REPEAT_INTERVAL):
        self.delay = delay
        self.interval = interval
        # key -> [seconds_held, seconds_since_last_repeat]
        self.timers = {}
    def press(self, key):
        """Register a fresh key press."""
        self.timers[key] = [0.0, 0.0]
    def release(self, key):
        """Forget a released key."""
        self.timers.pop(key, None)
    def release_all(self):
        """Forget every held key (used on pause/restart/game over)."""
        self.timers.clear()
    def update(self, dt):
        """Advance timers; return the keys that should fire a repeat now."""
        fired = []
        for key in list(self.timers.keys()):
            held, since = self.timers[key]
            held += dt
            since += dt
            if held >= self.delay and since >= self.interval:
                since = 0.0
                fired.append(key)
            self.timers[key] = [held, since]
        return fired
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen)
    repeater = InputRepeater()
    # keys that auto-repeat while held: key -> (method_name, argument)
    repeat_actions = {
        pygame.K_LEFT: ('move_horizontal', -1),
        pygame.K_RIGHT: ('move_horizontal', 1),
        pygame.K_DOWN: ('soft_drop', None),
    }
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                    repeater.release_all()
                elif event.key == pygame.K_r:
                    game.restart()
                    repeater.release_all()
                elif event.key == pygame.K_UP:
                    game.rotate(1)
                elif event.key == pygame.K_z:
                    game.rotate(-1)
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                    repeater.release_all()
                elif event.key in repeat_actions:
                    repeater.press(event.key)
                    action, arg = repeat_actions[event.key]
                    if arg is None:
                        getattr(game, action)()
                    else:
                        getattr(game, action)(arg)
            elif event.type == pygame.KEYUP:
                repeater.release(event.key)
        # handle auto-repeat for held keys
        for key in repeater.update(dt):
            if game.game_over or game.paused:
                repeater.release_all()
                break
            action, arg = repeat_actions[key]
            if arg is None:
                getattr(game, action)()
            else:
                getattr(game, action)(arg)
        game.update(dt)
        renderer.draw(game)
    pygame.quit()
if __name__ == '__main__':
    main()