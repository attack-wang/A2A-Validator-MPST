'''Alien sprite for the Space Invaders game.'''
import pygame
from settings import (ALIEN_ROWS, ALIEN_COLS, ALIEN_WIDTH, ALIEN_HEIGHT,
                      ALIEN_HORIZONTAL_SPACING, ALIEN_VERTICAL_SPACING,
                      ALIEN_TOP_MARGIN, ALIEN_LEFT_MARGIN,
                      ALIEN_ANIMATION_FRAMES, ALIEN_ROW_POINTS,
                      ALIEN_COLORS, BLACK)
class Alien(pygame.sprite.Sprite):
    '''A single alien in the formation. Uses float coordinates for smooth
    movement; horizontal/drop motion is driven by Game.move_aliens.'''
    def __init__(self, game, row, col):
        super().__init__()
        self.game = game
        self.row = row
        self.col = col
        self.points = ALIEN_ROW_POINTS[row % len(ALIEN_ROW_POINTS)]
        self.color = ALIEN_COLORS[row % len(ALIEN_COLORS)]
        self.frames = self._make_frames()
        self.frame_index = 0
        self.image = self.frames[0]
        x = ALIEN_LEFT_MARGIN + col * (ALIEN_WIDTH + ALIEN_HORIZONTAL_SPACING)
        y = ALIEN_TOP_MARGIN + row * (ALIEN_HEIGHT + ALIEN_VERTICAL_SPACING)
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect = self.image.get_rect(topleft=(x, y))
    def _make_frames(self):
        w, h = ALIEN_WIDTH, ALIEN_HEIGHT
        color = self.color
        frames = []
        for leg_out in (True, False):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(surf, color, (6, 4, w - 12, h - 12), border_radius=6)
            pygame.draw.circle(surf, BLACK, (int(w * 0.35), int(h * 0.45)), 3)
            pygame.draw.circle(surf, BLACK, (int(w * 0.65), int(h * 0.45)), 3)
            if leg_out:
                pygame.draw.line(surf, color, (8, h - 8), (2, h - 2), 2)
                pygame.draw.line(surf, color, (w - 8, h - 8), (w - 2, h - 2), 2)
            else:
                pygame.draw.line(surf, color, (8, h - 8), (10, h - 2), 2)
                pygame.draw.line(surf, color, (w - 8, h - 8), (w - 10, h - 2), 2)
            frames.append(surf)
        return frames
    def update(self):
        # Animation only; movement handled by Game.move_aliens
        self.frame_index = (self.game.frame_count // ALIEN_ANIMATION_FRAMES) % 2
        self.image = self.frames[self.frame_index]
    def move(self, dx, dy=0):
        self.pos_x += dx
        self.pos_y += dy
        self.rect.topleft = (round(self.pos_x), round(self.pos_y))