'''
main.py
Entry point for the Tetris game: initialises pygame, creates the game,
renderer and input-state objects, then runs the main loop at a fixed
frame rate, dispatching keyboard events and per-frame updates.
'''
import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game
from renderer import Renderer
from inputstate import InputState
def handle_keydown(event, game, input_state):
    '''Translate a KEYDOWN event into the corresponding game action.'''
    if game.game_over:
        # Only restart is accepted once the game has ended.
        if event.key == pygame.K_r:
            game.restart()
            input_state.reset()
        return
    if event.key in (pygame.K_UP, pygame.K_x):
        game.rotate(1)          # rotate clockwise
    elif event.key == pygame.K_z:
        game.rotate(-1)         # rotate counter-clockwise
    elif event.key == pygame.K_SPACE:
        game.hard_drop()
    elif event.key == pygame.K_p:
        game.toggle_pause()
        input_state.reset()
    elif event.key == pygame.K_r:
        game.restart()
        input_state.reset()
def main():
    '''Initialise pygame and run the game loop until the window closes.'''
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    game = Game()
    renderer = Renderer(screen, game)
    input_state = InputState(game)
    running = True
    while running:
        # dt in seconds, capped by the target frame rate.
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    handle_keydown(event, game, input_state)
        # Held-key auto-repeat (movement / soft drop), then gravity.
        input_state.update(dt)
        game.update(dt)
        renderer.draw()
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()