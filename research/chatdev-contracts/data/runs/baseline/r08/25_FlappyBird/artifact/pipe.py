'''
Pipe entity: random gap generation, movement, collision, and rendering.
'''
import random
import pygame
import settings
class Pipe:
    '''A vertical pipe pair with a random gap the bird must fly through.'''
    def __init__(self, x, gap_center, gap_size):
        '''Initialize pipe position, gap geometry, and scoring flag.'''
        self.x = x
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.scored = False
        self.gap_top = gap_center - gap_size / 2
        self.gap_bottom = gap_center + gap_size / 2
    @staticmethod
    def random_gap_center(gap_size):
        '''Return a random vertical center for a gap, keeping pipes on-screen.'''
        margin = 60
        min_center = margin + gap_size / 2
        max_center = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - margin - gap_size / 2
        if min_center > max_center:
            return (min_center + max_center) / 2
        return random.uniform(min_center, max_center)
    def update(self, dt, speed):
        '''Move the pipe leftward at the given speed.'''
        self.x -= speed * dt
    def is_offscreen(self):
        '''Return True when the pipe has fully scrolled off the left edge.'''
        return self.x + settings.PIPE_WIDTH < -settings.PIPE_CAP_OVERHANG
    def collides_with(self, rect):
        '''Return True if the given rect intersects either pipe section.'''
        cap_w = settings.PIPE_WIDTH + settings.PIPE_CAP_OVERHANG * 2
        top_shaft = pygame.Rect(int(self.x), 0, settings.PIPE_WIDTH,
                                int(self.gap_top - settings.PIPE_CAP_HEIGHT))
        top_cap = pygame.Rect(int(self.x) - settings.PIPE_CAP_OVERHANG,
                              int(self.gap_top - settings.PIPE_CAP_HEIGHT),
                              cap_w, settings.PIPE_CAP_HEIGHT)
        bottom_shaft = pygame.Rect(int(self.x), int(self.gap_bottom + settings.PIPE_CAP_HEIGHT),
                                   settings.PIPE_WIDTH, settings.SCREEN_HEIGHT)
        bottom_cap = pygame.Rect(int(self.x) - settings.PIPE_CAP_OVERHANG,
                                 int(self.gap_bottom), cap_w, settings.PIPE_CAP_HEIGHT)
        for section in (top_shaft, top_cap, bottom_shaft, bottom_cap):
            if section.colliderect(rect):
                return True
        return False
    def has_passed(self, bird_x):
        '''Return True if the bird has passed this pipe (for scoring).'''
        return not self.scored and self.x + settings.PIPE_WIDTH < bird_x - settings.BIRD_RADIUS
    def mark_scored(self):
        '''Flag this pipe so it can only be scored once.'''
        self.scored = True
    def draw(self, screen):
        '''Render the pipe pair with shafts and caps.'''
        cap_w = settings.PIPE_WIDTH + settings.PIPE_CAP_OVERHANG * 2
        cap_x = int(self.x) - settings.PIPE_CAP_OVERHANG
        # top pipe
        top_shaft_height = int(self.gap_top - settings.PIPE_CAP_HEIGHT)
        pygame.draw.rect(screen, settings.PIPE_GREEN,
                         (int(self.x), 0, settings.PIPE_WIDTH, top_shaft_height))
        pygame.draw.rect(screen, settings.PIPE_DARK,
                         (int(self.x), 0, settings.PIPE_WIDTH, top_shaft_height), 2)
        # highlight stripe
        pygame.draw.rect(screen, settings.PIPE_LIGHT, (int(self.x) + 6, 0, 8, top_shaft_height))
        # cap
        pygame.draw.rect(screen, settings.PIPE_GREEN,
                         (cap_x, int(self.gap_top - settings.PIPE_CAP_HEIGHT),
                          cap_w, settings.PIPE_CAP_HEIGHT))
        pygame.draw.rect(screen, settings.PIPE_DARK,
                         (cap_x, int(self.gap_top - settings.PIPE_CAP_HEIGHT),
                          cap_w, settings.PIPE_CAP_HEIGHT), 2)
        # bottom pipe
        bottom_top = int(self.gap_bottom + settings.PIPE_CAP_HEIGHT)
        pygame.draw.rect(screen, settings.PIPE_GREEN,
                         (int(self.x), bottom_top, settings.PIPE_WIDTH,
                          settings.SCREEN_HEIGHT - bottom_top))
        pygame.draw.rect(screen, settings.PIPE_DARK,
                         (int(self.x), bottom_top, settings.PIPE_WIDTH,
                          settings.SCREEN_HEIGHT - bottom_top), 2)
        pygame.draw.rect(screen, settings.PIPE_LIGHT,
                         (int(self.x) + 6, bottom_top, 8, settings.SCREEN_HEIGHT - bottom_top))
        pygame.draw.rect(screen, settings.PIPE_GREEN,
                         (cap_x, int(self.gap_bottom), cap_w, settings.PIPE_CAP_HEIGHT))
        pygame.draw.rect(screen, settings.PIPE_DARK,
                         (cap_x, int(self.gap_bottom), cap_w, settings.PIPE_CAP_HEIGHT), 2)