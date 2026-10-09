"""HUD and text rendering helpers."""
import pygame
import settings
def load_fonts():
    return {
        "small": pygame.font.Font(None, settings.FONT_SMALL),
        "medium": pygame.font.Font(None, settings.FONT_MEDIUM),
        "large": pygame.font.Font(None, settings.FONT_LARGE),
    }
def draw_text(surface, text, font, color, center=None, topleft=None):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center is not None:
        rect.center = center
    if topleft is not None:
        rect.topleft = topleft
    surface.blit(rendered, rect)
def draw_hud(surface, fonts, score, high_score, lives, ship_image):
    draw_text(surface, f"SCORE: {score}", fonts["medium"], settings.COLOR_WHITE, topleft=(16, 10))
    draw_text(surface, f"HI-SCORE: {high_score}", fonts["medium"], settings.COLOR_GREY, topright=(settings.SCREEN_WIDTH - 16, 10))
    # lives as ship icons
    for i in range(lives):
        surface.blit(ship_image, (16 + i * (ship_image.get_width() + 8), settings.SCREEN_HEIGHT - ship_image.get_height() - 10))
    draw_text(surface, f"LIVES: {lives}", ...)