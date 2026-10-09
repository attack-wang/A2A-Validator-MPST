'''Button module: clickable UI button with hover/enable states.'''
import pygame
import ui
import config
class Button:
    def __init__(self, text, x, y, width, height, callback=None, font_size=22):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.font_size = font_size
        self.enabled = True
        self.hovered = False
    def set_enabled(self, enabled):
        self.enabled = enabled
    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)
    def update_hover(self, pos):
        self.hovered = self.enabled and self.rect.collidepoint(pos)
    def draw(self, surface, font_size=None):
        size = font_size if font_size is not None else self.font_size
        base = (60, 70, 110) if self.enabled else (40, 44, 60)
        if self.hovered and self.enabled:
            base = (80, 95, 145)
        pygame.draw.rect(surface, base, self.rect, border_radius=10)
        pygame.draw.rect(surface, config.BOARD_BORDER_COLOR, self.rect, 2, border_radius=10)
        color = config.TEXT_COLOR if self.enabled else config.TEXT_DIM_COLOR
        ui.draw_text(surface, self.text, size, color, self.rect.centerx, self.rect.centery, anchor="center", bold=True)
    def on_click(self):
        if self.enabled and self.callback:
            self.callback()