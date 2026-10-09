'''
main.py
Main entry point for the Tetris game: initializes pygame, runs the game
loop with input handling (including key auto-repeat), and offers a
restart/quit screen after game over. Requires the pygame package
(install with: pip install pygame, or pip install -r requirements.txt).
'''
import sys
# Import pygame defensively: if the dependency is missing, print a clear,
# actionable message and exit cleanly instead of raising a raw traceback.
try:
    import pygame
except ImportError:
    print("Error: the required package 'pygame' is not installed.")
    print("Install it by running:  pip install pygame")
    print("Or install all dependencies with:  pip install -r requirements.txt")
    sys.exit(1)
from game import Game
from renderer import Renderer
from input_handler import InputRepeater
from constants import FPS
# Keys that auto-repeat while held (horizontal movement and soft drop).
REPEAT_KEYS = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN}
def handle_keydown(game, key):
    """Translate a key press into the corresponding game action."""
    if key == pygame.K_LEFT:
        game.move_left()
    elif key == pygame.K_RIGHT:
        game.move_right()
    elif key == pygame.K_DOWN:
        game.soft_drop()
    elif key == pygame.K_UP:
        game.rotate()
    elif key == pygame.K_SPACE:
        game.hard_drop()
def game_over_loop(renderer):
    """
    Show the game-over screen until the player chooses an option.
    Restart on R; exit the program on Q or window close.
    """
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        renderer.draw()
        clock.tick(30)
def main():
    """Program entry point: initialize pygame and run game sessions."""
    pygame.init()
    while True:
        game = Game()
        renderer = Renderer(game)
        clock = pygame.time.Clock()
        repeater = InputRepeater()
        # Main gameplay loop: runs until no more pieces can be placed.
        while not game.game_over:
            dt = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Only movement keys participate in auto-repeat.
                    if event.key in REPEAT_KEYS:
                        repeater.press(event.key)
                    handle_keydown(game, event.key)
                elif event.type == pygame.KEYUP:
                    repeater.release(event.key)
            # Handle auto-repeat for held movement keys.
            for key in repeater.update(dt):
                handle_keydown(game, key)
            game.update(dt)
            renderer.draw()
        # Game-over screen: restart on R, exit on Q or window close.
        game_over_loop(renderer)
if __name__ == "__main__":
    main()