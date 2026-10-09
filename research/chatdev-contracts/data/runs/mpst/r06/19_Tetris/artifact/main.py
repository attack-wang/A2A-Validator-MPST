'''
Main entry point for the Tetris game. Initializes pygame and runs the game loop.
'''
import sys
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE
from game import Game
from renderer import Renderer
from input_handler import InputHandler
def main():
    '''Initialize pygame, create game objects and run the main loop.'''
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen)
    input_handler = InputHandler(game)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                action = input_handler.handle_event(event)
                if action == 'quit':
                    running = False
        game.update(dt)
        renderer.draw(game)
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()