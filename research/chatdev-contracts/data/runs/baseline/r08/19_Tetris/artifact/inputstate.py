'''
inputstate.py
Handles keyboard input with DAS/ARR auto-repeat for horizontal movement and
auto-repeat for soft drop, translating raw key state into game actions.
'''
import pygame
from constants import DAS_DELAY, ARR_INTERVAL, SOFT_DROP_INTERVAL
class InputState:
    '''Tracks held-key state and fires repeated game actions (DAS/ARR).'''
    def __init__(self, game):
        self.game = game
        self.last_direction = 0
        self.das_timer = 0.0
        self.arr_timer = 0.0
        self.soft_timer = 0.0
    def reset(self):
        '''Clear all repeat timers (used on pause / game over / release).'''
        self.last_direction = 0
        self.das_timer = 0.0
        self.arr_timer = 0.0
        self.soft_timer = 0.0
    def update(self, dt):
        '''Poll the keyboard each frame and apply held-key actions.'''
        keys = pygame.key.get_pressed()
        if self.game.game_over or self.game.paused:
            self.reset()
            return
        # -- horizontal movement with DAS/ARR -----------------------------
        direction = 0
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            direction = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            direction = 1
        if direction != self.last_direction:
            # New press (or release): move once immediately, restart timers.
            self.last_direction = direction
            self.das_timer = 0.0
            self.arr_timer = 0.0
            if direction != 0:
                self.game.move(direction, 0)
        elif direction != 0:
            self.das_timer += dt
            if self.das_timer >= DAS_DELAY:
                self.arr_timer += dt
                while self.arr_timer >= ARR_INTERVAL:
                    self.arr_timer -= ARR_INTERVAL
                    self.game.move(direction, 0)
        # -- soft drop auto-repeat ----------------------------------------
        if keys[pygame.K_DOWN]:
            self.soft_timer += dt
            while self.soft_timer >= SOFT_DROP_INTERVAL:
                self.soft_timer -= SOFT_DROP_INTERVAL
                self.game.soft_drop()
        else:
            self.soft_timer = 0.0