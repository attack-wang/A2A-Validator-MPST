'''
main.py
Entry point for the 2048 game. Tries to start the pygame-based graphical
version; if pygame is not installed, it automatically falls back to a
console version so the game always runs without external dependencies.
'''
from game import Game
from constants import UP, DOWN, LEFT, RIGHT
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
def run_graphical():
    '''Run the pygame-based graphical version of the game.'''
    from renderer import Renderer
    from input_handler import InputHandler
    renderer = Renderer()
    game = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_q:
                    running = False
                else:
                    direction = InputHandler.get_direction(event)
                    if direction and not game.game_over:
                        game.move(direction)
        renderer.draw(game)
        clock.tick(60)
    pygame.quit()
def run_console():
    '''Run the terminal-based fallback version of the game.'''
    from console_renderer import (ConsoleRenderer, read_key,
                                  ACTION_RESTART, ACTION_QUIT)
    game = Game()
    renderer = ConsoleRenderer()
    renderer.draw(game)
    while True:
        action = read_key()
        if action == ACTION_QUIT:
            break
        if action == ACTION_RESTART:
            game.reset()
        elif action in (UP, DOWN, LEFT, RIGHT) and not game.game_over:
            game.move(action)
        renderer.draw(game)
def main():
    '''Choose the best available frontend and run the game loop.'''
    if PYGAME_AVAILABLE:
        run_graphical()
    else:
        print('pygame is not installed - starting console mode instead.')
        print('Run "pip install pygame" to enable the graphical version.')
        run_console()
if __name__ == '__main__':
    main()