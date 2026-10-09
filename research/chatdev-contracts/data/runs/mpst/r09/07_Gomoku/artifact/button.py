'''
button.py
Standalone reusable Button widget with a hover effect.
NOTE: gui.py already contains the Button implementation actually used by
the game; this module is kept as a standalone reusable copy and now
imports everything it needs so it no longer raises NameError.
'''
import pygame
from config import COLOR_BUTTON, COLOR_BUTTON_HOVER
class Button:
    """A simple clickable button with hover effect."""
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
    def update(self, mouse_pos):
        """Refresh the hover state; call once per frame."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    def handle_event(self, event):
        """Return True if the button was clicked inside this event."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False
    def draw(self, surface):
        """Render the button onto the given surface."""
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        label = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=self.rect.center))