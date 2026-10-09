"""
ui.py
Rendering helpers for HUD, board frame, buttons and game-over overlay.
"""
import pygame
from constants import (
    WINDOW_WIDTH, GRID_SIZE, CELL_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y,
    BOARD_PIXEL_SIZE, TARGET_SCORE, INITIAL_MOVES,
    COLOR_BACKGROUND, COLOR_BOARD_A, COLOR_BOARD_B, COLOR_BOARD_BORDER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT, COLOR_PANEL,
    COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_GAME_OVER_BG, COLOR_SELECTION,
)
_font_cache = {}
def get_font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        font = pygame.font.Font(None, size)
        font.set_bold(bold)
        _font_cache[key] = font
    return _font_cache[key]
def draw_hud(surface, score, moves_left, combo):
    panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, BOARD_OFFSET_Y - 12)
    pygame.draw.rect(surface, COLOR_PANEL, panel_rect)
    # title
    title = get_font(34, True).render("Candy Match", True, COLOR_ACCENT)
    surface.blit(title, (BOARD_OFFSET_X, 12))
    # score
    small = get_font(24)
    score_text = small.render(f"Score: {score}", True, COLOR_TEXT)
    surface.blit(score_text, (BOARD_OFFSET_X, 56))
    target_text = small.render(f"Target: {TARGET_SCORE}", True, COLOR_TEXT_DIM)
    surface.blit(target_text, (BOARD_OFFSET_X, 86))
    # moves (right side)
    moves_color = COLOR_ACCENT if moves_left <= 5 else COLOR_TEXT
    moves_text = small.render(f"Moves: {moves_left}", True, moves_color)
    surface.blit(moves_text, (BOARD_OFFSET_X + BOARD_PIXEL_SIZE - moves_text.get_width(), 56))
    # combo
    if combo > 1:
        combo_text = get_font(24, True).render(f"Combo x{combo}!", True, COLOR_ACCENT)
        surface.blit(combo_text, (BOARD_OFFSET_X + BOARD_PIXEL_SIZE - combo_text.get_width(), 86))