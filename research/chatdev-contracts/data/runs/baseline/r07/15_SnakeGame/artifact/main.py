'''
main.py
Entry point: pygame initialisation, main-menu loop and game sessions.
'''
import sys
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    DIFFICULTY_ORDER, DIFFICULTY_LEVELS,
    BLACK, GRAY, GREEN, WHITE, GRID_LINE, DARK_GRAY,
)
from game import Game
from ui import draw_text, menu_button_rects
from storage import load_high_scores
def _render_menu(screen, selected, high_scores):
    '''Draw the difficulty-selection menu screen.'''
    screen.fill(BLACK)
    draw_text(screen, "S N A K E", 56, GREEN, center=(WINDOW_WIDTH // 2, 70))
    draw_text(screen, "Classic Snake — choose your difficulty", 18, GRAY,
              center=(WINDOW_WIDTH // 2, 115))
    rects = menu_button_rects()
    for i, name in enumerate(DIFFICULTY_ORDER):
        cfg = DIFFICULTY_LEVELS[name]
        rect = rects[i]
        is_selected = (i == selected)
        pygame.draw.rect(screen, DARK_GRAY if is_selected else (30, 30, 30),
                         rect, border_radius=8)
        pygame.draw.rect(screen, cfg["color"] if is_selected else GRID_LINE,
                         rect, 2, border_radius=8)
        label = (f"{name}  (speed {cfg['fps']}  x{cfg['multiplier']} points)"
                 f"   Best: {high_scores.get(name, 0)}")
        draw_text(screen, label, 20, WHITE if is_selected else GRAY,
                  center=rect.center)
    draw_text(screen, "Arrows/W-S: select   Enter: play   Esc: quit", 16, GRAY,
              center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
    pygame.display.flip()
def run_menu(screen):
    '''Menu loop; returns the chosen difficulty name, or None to quit.'''
    selected = 0
    clock = pygame.time.Clock()
    high_scores = load_high_scores()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(DIFFICULTY_ORDER)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(DIFFICULTY_ORDER)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return DIFFICULTY_ORDER[selected]
                elif event.key == pygame.K_ESCAPE:
                    return None
        _render_menu(screen, selected, high_scores)
        clock.tick(30)
def main():
    '''Application entry point.'''
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    try:
        while True:
            difficulty = run_menu(screen)
            if difficulty is None:
                break
            action = Game(difficulty).run(screen)
            if action == "quit":
                break
            # "menu" loops back to the selection screen
    finally:
        pygame.quit()
        sys.exit(0)
if __name__ == "__main__":
    main()