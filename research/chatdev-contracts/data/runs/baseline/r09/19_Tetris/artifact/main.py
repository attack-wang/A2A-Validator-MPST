'''
main.py
Entry point of the Tetris game: wires the Game (rules engine) and the
UI (pygame rendering) together and runs the main event loop, handling
keyboard input (move, rotate, soft/hard drop, pause, restart, quit)
and advancing gravity each frame.
'''
import sys
import pygame
from game import Game
from ui import UI
def run():
    """Create the game and UI, then run the main loop until quit."""
    game = Game()
    ui = UI(game)
    running = True
    while running:
        dt = ui.clock.tick(60)  # ms since last frame, feeds gravity
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    game.move_horizontal(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move_horizontal(1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_DOWN:
                    game.soft_drop()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_p:
                    game.paused = not game.paused
                elif event.key == pygame.K_r:
                    game.reset()
        game.update(dt)
        ui.draw()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    run()