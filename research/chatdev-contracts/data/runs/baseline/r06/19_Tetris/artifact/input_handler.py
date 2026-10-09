'''
input_handler.py
Translates keyboard events into game actions.
'''
import pygame
from game import Game
class InputHandler:
    """Maps pygame key events to Tetris game actions."""
    def handle_events(self, game):
        """Process the pygame event queue and apply actions to the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    game.restart()
                    continue
                if event.key == pygame.K_p:
                    game.toggle_pause()
                    continue
                if game.game_over:
                    continue
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.soft_drop()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
        return True