'''
ui.py
Reusable UI helpers: text rendering, score display, grid drawing,
and overlay screens (pause / game over).
'''
import pygame
import settings
def draw_text(surface, text, size, color, center=None, topleft=None, topright=None, bold=False):
    """Render a text string onto the surface at the requested position."""
    font = pygame.font.SysFont("consolas", size, bold=bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    if topleft is not None:
        rect.topleft = topleft
    if topright is not None:
        rect.topright = topright
    surface.blit(rendered, rect)
    return rect
def draw_grid(surface):
    """Draw a subtle grid over the whole playfield."""
    for x in range(0, settings.WINDOW_WIDTH, settings.GRID_SIZE):
        pygame.draw.line(surface, settings.COLOR_GRID, (x, 0), (x, settings.WINDOW_HEIGHT))
    for y in range(0, settings.WINDOW_HEIGHT, settings.GRID_SIZE):
        pygame.draw.line(surface, settings.COLOR_GRID, (0, y), (settings.WINDOW_WIDTH, y))
def draw_border(surface):
    """Draw a frame around the playfield to visualise the deadly boundary."""
    border_rect = pygame.Rect(0, 0, settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
    pygame.draw.rect(surface, settings.COLOR_BORDER, border_rect, 2)
def draw_score(surface, score, high_score, difficulty_name):
    """Display the current score, best score and active difficulty."""
    draw_text(
        surface,
        f"Score: {score}",
        20,
        settings.COLOR_TEXT,
        topleft=(10, 8),
        bold=True,
    )
    draw_text(
        surface,
        f"Best: {high_score}",
        20,
        settings.COLOR_TEXT_DIM,
        topright=(settings.WINDOW_WIDTH - 10, 8),
    )
    draw_text(
        surface,
        f"Difficulty: {difficulty_name}",
        16,
        settings.COLOR_TEXT_DIM,
        topright=(settings.WINDOW_WIDTH - 10, 32),
    )
def draw_center_message(surface, lines):
    """Draw a stack of centered text lines (used for overlays)."""
    line_height = 36
    start_y = settings.WINDOW_HEIGHT // 2 - (len(lines) - 1) * line_height // 2
    for i, line in enumerate(lines):
        size = 32 if i == 0 else 18
        color = settings.COLOR_GAME_OVER if i == 0 else settings.COLOR_TEXT
        draw_text(
            surface,
            line,
            size,
            color,
            center=(settings.WINDOW_WIDTH // 2, start_y + i * line_height),
        )