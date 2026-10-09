'''
Input handler translating pygame key events into game actions.
'''
import pygame
from config import KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL
class InputHandler:
    '''Maps keyboard events to Tetris game commands.'''
    def __init__(self, game):
        self.game = game
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
    def handle_event(self, event):
        '''Process a single pygame event; returns True if the game state changed.'''
        if event.type != pygame.KEYDOWN:
            return False
        game = self.game
        if game.game_over:
            if event.key == pygame.K_r:
                game.restart()
                return True
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'quit'
            return False
        if event.key == pygame.K_LEFT:
            game.move_left()
            return True
        elif event.key == pygame.K_RIGHT:
            game.move_right()
            return True
        elif event.key == pygame.K_DOWN:
            game.soft_drop()
            return True
        elif event.key == pygame.K_UP:
            game.rotate()
            return True
        elif event.key == pygame.K_SPACE:
            game.hard_drop()
            return True
        elif event.key == pygame.K_p:
            game.toggle_pause()
            return True
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            return 'quit'
        return False