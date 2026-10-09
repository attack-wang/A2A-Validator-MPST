'''
input_handler.py
Keyboard input handling for the 2048 game.
'''
import pygame
from constants import UP, DOWN, LEFT, RIGHT
class InputHandler:
    '''Translates pygame keyboard events into game actions.'''
    @staticmethod
    def get_direction(event):
        '''Return the movement direction for an arrow key event, or None.'''
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                return UP
            if event.key in (pygame.K_DOWN, pygame.K_s):
                return DOWN
            if event.key in (pygame.K_LEFT, pygame.K_a):
                return LEFT
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                return RIGHT
        return None