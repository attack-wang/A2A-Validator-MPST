'''
ui.py
Rendering helpers: draws the board grid, falling piece, locked cells,
next-piece preview, the sidebar with score/level/lines, and overlay
messages (pause / game over).
'''
import pygame
from constants import (BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, SIDEBAR_WIDTH,
                       WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GRAY,
                       DARK_GRAY, GRID_COLOR, BORDER_COLOR, TEXT_COLOR,
                       ACCENT_COLOR, OVERLAY_COLOR)
def draw_cell(surface, x, y, color, size=CELL_SIZE, border=True):
    """Draw a single square cell at pixel position (x, y)."""
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, color, rect)
    if border:
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # small highlight for a beveled look
        light = tuple(min(255, ch + 60) for ch in color)
        pygame.draw.line(surface, light, (x + 1, y + 1), (x + size - 2, y + 1))
        pygame.draw.line(surface, light, (x + 1, y + 1), (x + 1, y + size - 2))
def draw_board(surface, board):
    """Draw the playfield background, grid lines, locked cells and border."""
    board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
    pygame.draw.rect(surface, DARK_GRAY, board_rect)
    # grid lines
    for x in range(0, BOARD_WIDTH * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, BOARD_HEIGHT * CELL_SIZE))
    for y in range(0, BOARD_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (BOARD_WIDTH * CELL_SIZE, y))
    # locked cells
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            color = board.grid[r][c]
            if color is not None:
                draw_cell(surface, c * CELL_SIZE, r * CELL_SIZE, color)
    # border
    pygame.draw.rect(surface, BORDER_COLOR, board_rect, 2)
def draw_piece(surface, piece):
    """Draw the currently falling piece on the playfield."""
    for x, y in piece.cells():
        if y >= 0:
            draw_cell(surface, x * CELL_SIZE, y * CELL_SIZE, piece.color)
def draw_ghost_piece(surface, piece, board):
    """Draw a translucent outline showing where the piece would land."""
    dy = 0
    while board.is_valid_position(piece, 0, dy + 1):
        dy += 1
    if dy <= 0:
        return
    for x, y in piece.cells():
        if y + dy >= 0:
            rect = pygame.Rect(x * CELL_SIZE, (y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1)
def draw_next_preview(surface, piece, font):
    """Draw the next-piece preview box with the upcoming piece centered inside."""
    title = font.render("NEXT", True, TEXT_COLOR)
    box = pygame.Rect(0, 0, 4 * CELL_SIZE, 3 * CELL_SIZE)
    box.centerx = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH // 2
    box.top = 60
    pygame.draw.rect(surface, DARK_GRAY, box)
    pygame.draw.rect(surface, BORDER_COLOR, box, 2)
    surface.blit(title, (box.centerx - title.get_width() // 2, box.top - title.get_height() - 6))
    if piece is None:
        return
    # Center the piece's filled cells inside the preview box
    cells = [(c, r) for r, row in enumerate(piece.matrix)
             for c, filled in enumerate(row) if filled]
    if not cells:
        return
    min_c = min(c for c, r in cells)
    max_c = max(c for c, r in cells)
    min_r = min(r for c, r in cells)
    max_r = max(r for c, r in cells)
    shape_w = (max_c - min_c + 1) * CELL_SIZE
    shape_h = (max_r - min_r + 1) * CELL_SIZE
    offset_x = box.centerx - shape_w // 2 - min_c * CELL_SIZE
    offset_y = box.centery - shape_h // 2 - min_r * CELL_SIZE
    for c, r in cells:
        draw_cell(surface, offset_x + c * CELL_SIZE, offset_y + r * CELL_SIZE, piece.color)
def draw_sidebar(surface, font, big_font, score, level, lines, next_piece):
    """Draw the right-hand info panel: score, level, lines and next piece."""
    sidebar_rect = pygame.Rect(BOARD_WIDTH * CELL_SIZE, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, BLACK, sidebar_rect)
    pygame.draw.line(surface, BORDER_COLOR,
                     (BOARD_WIDTH * CELL_SIZE, 0),
                     (BOARD_WIDTH * CELL_SIZE, WINDOW_HEIGHT), 2)
    center_x = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH // 2
    # Next piece preview
    draw_next_preview(surface, next_piece, font)
    # Score
    y = 60 + 3 * CELL_SIZE + 40
    score_title = font.render("SCORE", True, TEXT_COLOR)
    score_value = big_font.render(str(score), True, ACCENT_COLOR)
    surface.blit(score_title, (center_x - score_title.get_width() // 2, y))
    surface.blit(score_value, (center_x - score_value.get_width() // 2, y + 30))
    # Level
    y += 30 + big_font.get_height() + 20
    level_title = font.render("LEVEL", True, TEXT_COLOR)
    level_value = big_font.render(str(level), True, TEXT_COLOR)
    surface.blit(level_title, (center_x - level_title.get_width() // 2, y))
    surface.blit(level_value, (center_x - level_value.get_width() // 2, y + 30))
    # Lines
    y += 30 + big_font.get_height() + 20
    lines_title = font.render("LINES", True, TEXT_COLOR)
    lines_value = big_font.render(str(lines), True, TEXT_COLOR)
    surface.blit(lines_title, (center_x - lines_title.get_width() // 2, y))
    surface.blit(lines_value, (center_x - lines_value.get_width() // 2, y + 30))
    # Controls hint
    hints = [
        "LEFT/RIGHT: move",
        "DOWN: soft drop",
        "UP: rotate",
        "SPACE: hard drop",
        "P: pause",
        "R: restart",
        "ESC: quit",
    ]
    y += 30 + big_font.get_height() + 30
    small_font = pygame.font.Font(None, 22)
    for hint in hints:
        hint_surf = small_font.render(hint, True, GRAY)
        surface.blit(hint_surf, (center_x - hint_surf.get_width() // 2, y))
        y += 24
def draw_overlay(surface, font, huge_font, title, subtitle):
    """Draw a semi-transparent overlay with a title and subtitle message."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    surface.blit(overlay, (0, 0))
    title_surf = huge_font.render(title, True, WHITE)
    subtitle_surf = font.render(subtitle, True, TEXT_COLOR)
    center_y = WINDOW_HEIGHT // 2
    surface.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2,
                              center_y - title_surf.get_height()))
    surface.blit(subtitle_surf, (WINDOW_WIDTH // 2 - subtitle_surf.get_width() // 2,
                                 center_y + 20))