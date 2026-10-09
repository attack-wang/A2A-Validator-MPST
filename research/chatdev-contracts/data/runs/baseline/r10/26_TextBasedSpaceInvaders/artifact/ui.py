"""HUD and overlay text rendering."""
import pygame
import settings
def draw_hud(surface, font, score, lives, wave=None):
    score_text = font.render(f"Score: {score}", True, settings.WHITE)
    surface.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, settings.WHITE)
    surface.blit(lives_text, (settings.SCREEN_WIDTH - lives_text.get_width() - 10, 10))
    # draw life icons maybe
    wave_text = font.render(f"Wave: {wave}", True, settings.WHITE)
    surface.blit(wave_text, (settings.SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 10))
def draw_center_message(surface, big_font, font, title, subtitle, color):
    ...