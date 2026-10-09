'''
gui.py
Reusable widgets for the Minesweeper Pygame front-end.
...
'''
import pygame
from config import (COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_TEXT,
                    COLOR_BEVEL_DARK, COLOR_BEVEL_LIGHT,
                    COLOR_SMILEY, COLOR_SMILEY_BORDER, COLOR_SMILEY_EYE)
class Button:
    """A simple clickable rectangle with a centred text label."""
    def __init__(self, rect, label, action):
        self.rect = rect
        self.label = label
        self.action = action
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    def draw(self, surface, font, mouse_pos):
        color = COLOR_BUTTON_HOVER if self.is_hovered(mouse_pos) else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BEVEL_DARK, self.rect, 2, border_radius=8)
        label_surf = font.render(self.label, True, COLOR_BUTTON_TEXT)
        surface.blit(label_surf, label_surf.get_rect(center=self.rect.center))
class SmileyButton:
    """The classic smiley reset button; its face reflects the game state."""
    def __init__(self, rect):
        self.rect = rect
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    def draw(self, surface, game_won, game_lost, pressed=False, hovered=False):
        # button plate
        plate = self.rect.inflate(-6, -6)
        bg = COLOR_BEVEL_DARK if pressed else COLOR_SMILEY
        pygame.draw.rect(surface, bg, plate, border_radius=6)
        pygame.draw.rect(surface, COLOR_SMILEY_BORDER, plate, 2, border_radius=6)
        cx, cy = plate.center
        r = plate.width // 2 - 6
        # eyes
        eye_dx = r // 2
        eye_dy = -r // 3
        eye_r = max(2, r // 6)
        for sx in (-1, 1):
            pygame.draw.circle(surface, COLOR_SMILEY_EYE,
                               (cx + sx * eye_dx, cy + eye_dy), eye_r)
        # mouth: smile when playing/won, frown when lost, "o" when pressed
        if game_lost:
            # frown (arc opening downward)
            mouth_rect = pygame.Rect(cx - r // 2, cy + r // 5, r, r // 2)
            pygame.draw.arc(surface, COLOR_SMILEY_EYE, mouth_rect, 0, math.pi, 2)
        elif pressed:
            # surprised "o"
            pygame.draw.circle(surface, COLOR_SMILEY_EYE, (cx, cy + r // 3), max(2, r // 5))
        else:
            # smile
            mouth_rect = pygame.Rect(cx - r // 2, cy - r // 3, r, r // 2)
            pygame.draw.arc(surface, COLOR_SMILEY_EYE, mouth_rect, math.pi, 2 * math.pi, 2)