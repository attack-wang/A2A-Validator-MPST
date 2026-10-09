'''
main.py
Entry point of the Snake game. Initializes pygame, manages the
top-level states (difficulty menu -> playing -> game over), routes
keyboard events, and drives the main loop. The pygame import is
guarded so a missing dependency produces a clear, actionable
message instead of an unhandled ModuleNotFoundError traceback.
'''
import sys
try:
    import pygame
except ImportError:
    # Fixes the reported crash: ModuleNotFoundError: No module named 'pygame'.
    # Fail softly with an actionable hint instead of a raw traceback.
    print("Error: the required dependency 'pygame' is not installed.")
    print("Install it by running:  pip install pygame")
    sys.exit(1)
from settings import (
    SCREEN_WIDTH, WINDOW_HEIGHT, RENDER_FPS, DIFFICULTIES,
)
from game import Game
import ui
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
def main():
    """Initialize the game and run the main loop until the user quits."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake - ChatDev")
    clock = pygame.time.Clock()
    small_font = pygame.font.SysFont("consolas", 18, bold=True)
    big_font = pygame.font.SysFont("consolas", 40, bold=True)
    difficulty_names = list(DIFFICULTIES.keys())
    selected_index = 0
    state = MENU
    game = None
    paused = False
    high_score = 0
    running = True
    while running:
        # --- Timekeeping -------------------------------------------------
        delta_ms = clock.tick(RENDER_FPS)
        # --- Event handling ----------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected_index = (selected_index - 1) % len(difficulty_names)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected_index = (selected_index + 1) % len(difficulty_names)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game = Game(difficulty_names[selected_index])
                        paused = False
                        state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU
                        paused = False
                    else:
                        game.handle_event(event)
            elif state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        # --- Update -------------------------------------------------------
        if state == PLAYING and game is not None and not paused:
            game.update(delta_ms)
            if game.is_game_over():
                high_score = max(high_score, game.score)
                state = GAME_OVER
        # --- Render ---------------------------------------------------------
        if state == MENU:
            ui.draw_board(screen)
            ui.draw_start_menu(screen, big_font, small_font, selected_index)
        elif state == PLAYING and game is not None:
            game.render(screen, small_font, high_score)
            if paused:
                ui.draw_pause(screen, big_font, small_font)
        elif state == GAME_OVER and game is not None:
            game.render(screen, small_font, high_score)
            ui.draw_game_over(screen, big_font, small_font, game.score, game.won)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()