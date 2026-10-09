'''Alien enemies and drawing/animation logic.'''
import pygame
import settings
class Alien:
    def __init__(self, col, row, x, y):
        self.col = col
        self.row = row
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(int(x), int(y), settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT)
        self.points = settings.ALIEN_POINTS_BY_ROW[row % len(settings.ALIEN_POINTS_BY_ROW)]
        self.color = self._row_color(row)
        self.anim_timer = 0.0
        self.anim_frame = 0
    @staticmethod
    def _row_color(row):
        palette = [(255, 90, 90), (255, 160, 60), (255, 230, 80),
                   (120, 230, 120), (120, 180, 255)]
        return palette[row % len(palette)]
    def update(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (int(round(self.x)), int(round(self.y)))
    def animate(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= 0.4:
            self.anim_timer -= 0.4
            self.anim_frame = 1 - self.anim_frame
    def draw(self, screen):
        body = self.rect.inflate(-6, -6)
        pygame.draw.rect(screen, self.color, body, border_radius=4)
        # eyes
        eye_y = body.top + body.height // 3
        eye_h = 4
        if self.anim_frame == 0:
            eye_w = 6
            left_eye_x = body.left + 6
            right_eye_x = body.right - 6 - eye_w
        else:
            eye_w = 4
            left_eye_x = body.left + 8
            right_eye_x = body.right - 8 - eye_w
        pygame.draw.rect(screen, settings.COLOR_BACKGROUND, (left_eye_x, eye_y, eye_w, eye_h))
        pygame.draw.rect(screen, settings.COLOR_BACKGROUND, (right_eye_x, eye_y, eye_w, eye_h))
        # legs/antennae alternate by frame
        if self.anim_frame == 0:
            pygame.draw.rect(screen, self.color, (body.left + 4, body.bottom, 4, 4))
            pygame.draw.rect(screen, self.color, (body.right - 8, body.bottom, 4, 4))
        else:
            pygame.draw.rect(screen, self.color, (body.left + 10, body.bottom, 4, 4))
            pygame.draw.rect(screen, self.color, (body.right - 14, body.bottom, 4, 4))