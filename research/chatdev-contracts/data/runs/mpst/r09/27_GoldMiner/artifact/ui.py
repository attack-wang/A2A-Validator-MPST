'''
ui.py
HUD and overlay rendering helpers.
'''
import pygame
import config
def draw_text(surface, font, text, pos, color=config.COLOR_TEXT, shadow=True, align="topleft"):
    img = font.render(text, True, color)
    if shadow:
        sh = font.render(text, True, config.COLOR_TEXT_SHADOW)
        surface.blit(sh, (pos[0] + 2, pos[1] + 2))
    rect = img.get_rect(**{align: pos})
    surface.blit(img, rect)
def draw_hud(surface, font, small_font, level, score, target, time_left, last_grab_info=None):
    draw_text(surface, font, f"Level {level}", (10, 8))
    draw_text(surface, font, f"Gold: {score} / {target}", (10, 36))
    # timer with color warning
    color = config.COLOR_DANGER if time_left <= 10 else config.COLOR_TEXT
    draw_text(surface, font, f"Time: {time_left:0.1f}s",
              (config.SCREEN_WIDTH - 10, 8), color=color, align="topright")
    # progress bar
    bar_x, bar_y = config.SCREEN_WIDTH - 210, 40
    bar_w, bar_h = 200, 16
    pygame.draw.rect(surface, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h))
    frac = 0.0
    if target > 0:
        frac = max(0.0, min(1.0, score / target))
    fill_w = int(bar_w * frac)
    bar_color = config.COLOR_SUCCESS if frac >= 1.0 else config.COLOR_GOLD
    if fill_w > 0:
        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, fill_w, bar_h))
    pygame.draw.rect(surface, config.COLOR_TEXT_SHADOW, (bar_x, bar_y, bar_w, bar_h), 2)
    draw_text(surface, small_font, "Target", (bar_x, bar_y + bar_h + 2))
    # last grab info
    if last_grab_info:
        name, value = last_grab_info
        draw_text(surface, small_font, f"Last grab: {name} (+{value})",
                  (config.SCREEN_WIDTH - 10, 70), color=config.COLOR_SUCCESS, align="topright")
def draw_message(surface, font, text, center_pos, color=config.COLOR_TEXT):
    """Draw a centered message with a translucent backing panel."""
    if not text:
        return
    img = font.render(text, True, color)
    sh = font.render(text, True, config.COLOR_TEXT_SHADOW)
    rect = img.get_rect(center=center_pos)
    pad = 10
    panel = rect.inflate(pad * 2, pad)
    panel_surface = pygame.Surface(panel.size, pygame.SRCALPHA)
    panel_surface.fill(config.COLOR_OVERLAY)
    surface.blit(panel_surface, panel.topleft)
    surface.blit(sh, (rect.x + 2, rect.y + 2))
    surface.blit(img, rect.topleft)