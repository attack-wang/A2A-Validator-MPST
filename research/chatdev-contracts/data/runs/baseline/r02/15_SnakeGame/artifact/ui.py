'''
ui.py
Rendering helpers: text drawing, HUD/score display, board grid,
overlay screens (menu, pause, game over) and high-score persistence.
'''
import json
import os
import pygame
import settings
def get_font(size, bold=False):
    """Return a pygame Font, falling back to the default font."""
    try:
        font = pygame.font.SysFont(settings.FONT_NAME, size, bold=bold)
        if font is None:
            raise ValueError
        return font
    except Exception:
        return pygame.font.Font(None, size)
def draw_text(surface, text, size, color, center=None, topleft=None, topright=None, bold=False):
    """Blit `text` onto `surface`, anchored at `center`, `topleft` or `topright`."""
    font = get_font(size, bold)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    elif topright is not None:
        rect.topright = topright
    surface.blit(rendered, rect)
    return rect
def draw_board(surface, play_area_height):
    """Fill the background and draw the faint grid lines."""
    surface.fill(settings.COLOR_BACKGROUND)
    for x in range(0, settings.GRID_WIDTH * settings.GRID_SIZE, settings.GRID_SIZE):
        pygame.draw.line(surface, settings.COLOR_GRID_LINE, (x, 0), (x, play_area_height))
    for y in range(0, play_area_height, settings.GRID_SIZE):
        pygame.draw.line(surface, settings.COLOR_GRID_LINE, (0, y), (settings.GRID_WIDTH * settings.GRID_SIZE, y))
    pygame.draw.rect(
        surface,
        settings.COLOR_BORDER,
        pygame.Rect(0, 0, settings.GRID_WIDTH * settings.GRID_SIZE, play_area_height),
        2,
    )
def draw_hud(surface, score, high_score, difficulty, paused):
    """Draw the score bar underneath the playfield."""
    hud_rect = pygame.Rect(
        0,
        settings.GRID_HEIGHT * settings.GRID_SIZE,
        settings.WINDOW_WIDTH,
        settings.HUD_HEIGHT,
    )
    pygame.draw.rect(surface, settings.COLOR_HUD_BG, hud_rect)
    y_center = hud_rect.centery
    draw_text(surface, f"Score: {score}", settings.FONT_MEDIUM, settings.COLOR_TEXT, topleft=(10, y_center - 12), bold=True)
    draw_text(surface, f"High Score: {high_score}", settings.FONT_SMALL, settings.COLOR_TEXT_DIM, center=(settings.WINDOW_WIDTH // 2, y_center))
    draw_text(surface, f"{difficulty}" + ("  |  Paused" if paused else ""), settings.FONT_SMALL, settings.COLOR_TEXT_DIM, topright=(settings.WINDOW_WIDTH - 10, y_center - 8))
def draw_menu(surface, difficulty_names, selected_index):
    """Draw the main menu with difficulty selection."""
    surface.fill(settings.COLOR_BACKGROUND)
    center_x = settings.WINDOW_WIDTH // 2
    draw_text(surface, "SNAKE", settings.FONT_TITLE, settings.COLOR_MENU_HIGHLIGHT, center=(center_x, 70), bold=True)
    draw_text(surface, "ChatDev Edition", settings.FONT_MEDIUM, settings.COLOR_TEXT_DIM, center=(center_x, 110))
    draw_text(surface, "Select Difficulty", settings.FONT_MEDIUM, settings.COLOR_TEXT, center=(center_x, 160), bold=True)
    for index, name in enumerate(difficulty_names):
        preset = settings.DIFFICULTIES[name]
        label = f"{name}  (speed {preset['speed']}, x{preset['multiplier']} score)"
        if index == selected_index:
            draw_text(surface, f"> {label} <", settings.FONT_MEDIUM, settings.COLOR_MENU_HIGHLIGHT, center=(center_x, 200 + index * 34), bold=True)
        else:
            draw_text(surface, label, settings.FONT_MEDIUM, settings.COLOR_TEXT_DIM, center=(center_x, 200 + index * 34))
    draw_text(surface, "Up/Down or W/S to choose   Enter/Space to start", settings.FONT_SMALL, settings.COLOR_TEXT_DIM, center=(center_x, settings.WINDOW_HEIGHT - 50))
    draw_text(surface, "Esc to quit", settings.FONT_SMALL, settings.COLOR_TEXT_DIM, center=(center_x, settings.WINDOW_HEIGHT - 28))
def draw_pause(surface):
    """Draw a translucent pause overlay with instructions."""
    overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(settings.COLOR_OVERLAY)
    surface.blit(overlay, (0, 0))
    center_x = settings.WINDOW_WIDTH // 2
    center_y = settings.WINDOW_HEIGHT // 2
    draw_text(surface, "PAUSED", settings.FONT_LARGE, settings.COLOR_MENU_HIGHLIGHT, center=(center_x, center_y - 20), bold=True)
    draw_text(surface, "Press Space to resume", settings.FONT_SMALL, settings.COLOR_TEXT, center=(center_x, center_y + 20))
    draw_text(surface, "Press M for menu", settings.FONT_SMALL, settings.COLOR_TEXT_DIM, center=(center_x, center_y + 44))
def draw_game_over(surface, score, high_score, new_record, won):
    """Draw the game-over overlay with final score and restart hints."""
    overlay = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(settings.COLOR_OVERLAY)
    surface.blit(overlay, (0, 0))
    center_x = settings.WINDOW_WIDTH // 2
    center_y = settings.WINDOW_HEIGHT // 2
    title = "YOU WIN!" if won else "GAME OVER"
    draw_text(surface, title, settings.FONT_LARGE, settings.COLOR_MENU_HIGHLIGHT if won else settings.COLOR_FOOD, center=(center_x, center_y - 60), bold=True)
    draw_text(surface, f"Final Score: {score}", settings.FONT_MEDIUM, settings.COLOR_TEXT, center=(center_x, center_y - 15), bold=True)
    draw_text(surface, f"High Score: {high_score}", settings.FONT_SMALL, settings.COLOR_TEXT_DIM, center=(center_x, center_y + 12))
    if new_record:
        draw_text(surface, "*** NEW HIGH SCORE! ***", settings.FONT_SMALL, settings.COLOR_MENU_HIGHLIGHT, center=(center_x, center_y + 36), bold=True)
    draw_text(surface, "Enter/Space: play again   M: menu   Esc: quit", settings.FONT_SMALL, settings.COLOR_TEXT, center=(center_x, center_y + 66))
def load_high_score():
    """Read the persisted high score; return 0 if unavailable/corrupt."""
    try:
        with open(settings.HIGHSCORE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        score = int(data.get("high_score", 0))
        return max(0, score)
    except (FileNotFoundError, ValueError, TypeError, OSError):
        return 0
    except Exception:
        return 0
def save_high_score(score):
    """Persist the high score. Returns True if the file was written."""
    try:
        with open(settings.HIGHSCORE_FILE, "w", encoding="utf-8") as fh:
            json.dump({"high_score": int(score)}, fh)
        return True
    except (OSError, TypeError, ValueError):
        return False