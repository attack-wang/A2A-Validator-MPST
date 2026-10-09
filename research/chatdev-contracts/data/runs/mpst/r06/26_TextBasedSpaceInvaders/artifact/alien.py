'''Alien: a single invader in the descending fleet.'''
import pygame
class Alien:
    def __init__(self, settings, row, col):
        self.settings = settings
        self.row = row
        self.col = col
        self.points = settings.row_points[row]
        self.color = settings.row_colors[row]
        self.width = settings.alien_width
        self.height = settings.alien_height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.x = 0.0  # float position for smooth movement
        self.direction = 1
    def place_at(self, col_index, row_index):
        self.rect.x = self.settings.fleet_side_margin + col_index * self.settings.alien_x_spacing
        self.rect.y = self.settings.fleet_top_margin + row_index * self.settings.alien_y_spacing
        self.x = float(self.rect.x)
    def update(self, fleet_direction, drop_distance):
        self.x += fleet_direction * self.settings.alien_speed
        self.rect.x = int(self.x)
        if drop_distance:
            self.rect.y += drop_distance
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        # eyes
        eye_color = (15, 15, 15)
        eye_w, eye_h = 6, 8
        pygame.draw.rect(screen, eye_color, (self.rect.x + 8, self.rect.y + 7, eye_w, eye_h))
        pygame.draw.rect(screen, eye_color, (self.rect.right - 14, self.rect.y + 7, eye_w, eye_h))
        # mouth
        pygame.draw.rect(screen, eye_color, (self.rect.centerx - 6, self.rect.bottom - 9, 12, 4))