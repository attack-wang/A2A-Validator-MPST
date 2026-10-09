'''alien.py: alien enemies used to build the descending fleet rows.'''
import pygame
class Alien:
    def __init__(self, settings, row, col, x, y):
        self.settings = settings
        self.row = row
        self.col = col
        self.rect = pygame.Rect(x, y, settings.alien_width, settings.alien_height)
        self.x = float(self.rect.x)
        self.points = max(10, settings.alien_points_top - row * settings.alien_points_step)
        self.color = settings.alien_colors[row % len(settings.alien_colors)]
    def update(self, dx, dy):
        self.x += dx
        self.rect.x = int(self.x)
        if dy:
            self.rect.y += dy
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        # eyes
        eye_w = 6
        eye_h = 6
        eye_y = self.rect.y + self.rect.height // 3
        left_eye = pygame.Rect(self.rect.x + self.rect.width // 4 - eye_w // 2, eye_y, eye_w, eye_h)
        right_eye = pygame.Rect(self.rect.x + 3 * self.rect.width // 4 - eye_w // 2, eye_y, eye_w, eye_h)
        pygame.draw.rect(screen, (10, 12, 30), left_eye)
        pygame.draw.rect(screen, (10, 12, 30), right_eye)
        # mouth
        mouth = pygame.Rect(self.rect.x + self.rect.width // 4, self.rect.y + 2 * self.rect.height // 3, self.rect.width // 2, 4)
        pygame.draw.rect(screen, (10, 12, 30), mouth)