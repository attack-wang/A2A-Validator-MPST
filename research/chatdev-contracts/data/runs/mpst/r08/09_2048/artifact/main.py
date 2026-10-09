import pygame
from constants import ...
from game_logic import Game2048
from renderer import Renderer
import input_handler
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    game = Game2048()
    renderer = Renderer(screen)
    renderer.start_spawn_animation(game)  # initial pop-in of the two starting tiles? 
    running = True
    while running:
        now = pygame.time.get_ticks()
        events = pygame.event.get()
        if input_handler.quit_requested(events):
            running = False
            continue  # hmm, or break
        if input_handler.restart_requested(events):
            game.reset()
            renderer.reset_animation()
            renderer.start_new_game_animation(game)  # pop the two initial tiles
        direction = input_handler.get_move_direction(events)
        if direction:
            if game.won and not game.win_dismissed:
                game.win_dismissed = True
            if not game.game_over and game.move(direction):
                renderer.start_move_animation(game)
        renderer.draw(game, now)
        clock.tick(FPS)
    pygame.quit()