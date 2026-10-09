'''
input_handler.py
Translates keyboard input into game actions, with auto-repeat for held keys.
'''
import pygame
class InputHandler:
    """Maps pygame events and held keys to Tetris actions with DAS auto-repeat."""
    DAS_DELAY = 170   # ms a key must be held before auto-repeat starts
    ARR_DELAY = 45    # ms between auto-repeat moves
    def __init__(self):
        self.held = {}  # key -> {'timer': ms, 'action': method-name}
    def handle_events(self, game, dt):
        """Process events, update auto-repeat timers and apply actions."""
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    game.restart()
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                elif event.key == pygame.K_LEFT:
                    game.move_left()
                    self._start_repeat(pygame.K_LEFT, 'move_left')
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                    self._start_repeat(pygame.K_RIGHT, 'move_right')
                elif event.key == pygame.K_DOWN:
                    game.soft_drop()
                    self._start_repeat(pygame.K_DOWN, 'soft_drop')
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
            elif event.type == pygame.KEYUP:
                self.held.pop(event.key, None)
        self._update_repeat(game, dt)
        return running
    def _start_repeat(self, key, action):
        self.held[key] = {'timer': 0, 'action': action}
    def _update_repeat(self, game, dt):
        for key, state in self.held.items():
            state['timer'] += dt
            if state['timer'] >= self.DAS_DELAY:
                repeats = int((state['timer'] - self.DAS_DELAY) / self.ARR_DELAY)
                ...