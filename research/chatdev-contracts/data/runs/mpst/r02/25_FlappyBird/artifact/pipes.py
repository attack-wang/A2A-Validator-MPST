'''
Pipe and PipeManager classes: obstacles with random gaps and scaling difficulty.
'''
import random
import pygame
import settings
class Pipe:
    '''A single pipe pair (top and bottom) with a vertical gap.'''
    def __init__(self, x, gap_center, gap_height):
        self.x = float(x)
        self.gap_top = gap_center - gap_height / 2     # bottom edge of top pipe
        self.gap_bottom = gap_center + gap_height / 2  # top edge of bottom pipe
        self.passed = False
    def update(self, speed):
        '''Scroll the pipe pair to the left.'''
        self.x -= speed
    def has_passed(self, bird):
        '''Return True exactly once, when the bird clears this pipe (prevents double scoring).'''
        if self.passed:
            return False
        if bird.x - settings.BIRD_RADIUS > self.x + settings.PIPE_WIDTH:
            self.passed = True
            return True
        return False
    def is_offscreen(self):
        '''Return True once the pipe has fully left the left edge.'''
        return self.x + settings.PIPE_WIDTH + settings.PIPE_CAP_OVERHANG < 0
    def collides(self, bird_rect):
        '''Return True if the bird rect hits the top or bottom shaft.'''
        top = pygame.Rect(int(self.x), 0, settings.PIPE_WIDTH, max(0, int(self.gap_top)))
        bottom = pygame.Rect(int(self.x), int(self.gap_bottom), settings.PIPE_WIDTH,
                             max(0, settings.WINDOW_HEIGHT - int(self.gap_bottom)))
        return bird_rect.colliderect(top) or bird_rect.colliderect(bottom)
    def _draw_shaft(self, surface, x, top, height):
        '''Draw one vertical shaft with highlight and outline.'''
        shaft = pygame.Rect(int(x), int(top), settings.PIPE_WIDTH, max(0, int(height)))
        pygame.draw.rect(surface, settings.PIPE_BODY, shaft)
        pygame.draw.rect(surface, settings.PIPE_LIGHT, (shaft.x + 4, shaft.y + 2, 8, max(0, shaft.height - 4)))
        pygame.draw.rect(surface, settings.PIPE_OUTLINE, shaft, 2)
    def _draw_cap(self, surface, x, y):
        '''Draw the wider lip at the gap-facing end of a shaft.'''
        width = settings.PIPE_WIDTH + settings.PIPE_CAP_OVERHANG * 2
        cap = pygame.Rect(int(x) - settings.PIPE_CAP_OVERHANG, int(y), width, settings.PIPE_CAP_HEIGHT)
        pygame.draw.rect(surface, settings.PIPE_BODY, cap)
        pygame.draw.rect(surface, settings.PIPE_LIGHT, (cap.x + 4, cap.y + 3, 8, cap.height - 6))
        pygame.draw.rect(surface, settings.PIPE_OUTLINE, cap, 2)
    def draw(self, surface):
        '''Draw the top pipe (hanging into the gap) and bottom pipe (standing up to the gap).'''
        # Top pipe: shaft from the top of the screen, cap at its bottom end (gap-facing).
        self._draw_shaft(surface, self.x, 0, self.gap_top - settings.PIPE_CAP_HEIGHT)
        self._draw_cap(surface, self.x, self.gap_top - settings.PIPE_CAP_HEIGHT)
        # Bottom pipe: cap at its top end (gap-facing), shaft down to the screen bottom.
        self._draw_cap(surface, self.x, self.gap_bottom)
        self._draw_shaft(surface, self.x, self.gap_bottom + settings.PIPE_CAP_HEIGHT,
                         settings.WINDOW_HEIGHT - self.gap_bottom - settings.PIPE_CAP_HEIGHT)
class PipeManager:
    '''Spawns, moves and recycles pipes, and scales difficulty with the score.'''
    def __init__(self):
        self.pipes = []
    def reset(self):
        self.pipes = []
    @staticmethod
    def gap_height_for_score(score):
        '''Gap height shrinks as the score grows.'''
        t = min(score / settings.DIFFICULTY_SCORE, 1.0)
        return settings.BASE_GAP_HEIGHT - t * (settings.BASE_GAP_HEIGHT - settings.MIN_GAP_HEIGHT)
    @staticmethod
    def speed_for_score(score):
        '''Pipe speed increases as the score grows.'''
        t = min(score / settings.DIFFICULTY_SCORE, 1.0)
        return settings.BASE_PIPE_SPEED + t * (settings.MAX_PIPE_SPEED - settings.BASE_PIPE_SPEED)
    def _spawn_pipe(self, score):
        gap_height = self.gap_height_for_score(score)
        min_center = settings.GAP_MARGIN_TOP + gap_height / 2
        max_center = (settings.WINDOW_HEIGHT - settings.GROUND_HEIGHT
                      - settings.GAP_MARGIN_BOTTOM - gap_height / 2)
        gap_center = random.uniform(min_center, max_center)
        self.pipes.append(Pipe(settings.WINDOW_WIDTH + settings.PIPE_CAP_OVERHANG,
                               gap_center, gap_height))
    def update(self, score, bird):
        '''Move pipes, spawn new ones, remove offscreen ones and count passes.'''
        speed = self.speed_for_score(score)
        spawn_x = settings.WINDOW_WIDTH - settings.PIPE_SPACING
        if not self.pipes or self.pipes[-1].x < spawn_x:
            self._spawn_pipe(score)
        passed_count = 0
        for pipe in self.pipes:
            pipe.update(speed)
            if pipe.has_passed(bird):
                pipe.passed = True
                passed_count += 1
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
        return passed_count
    def collides(self, bird_rect):
        '''Return True if the bird rectangle hits any pipe.'''
        return any(pipe.collides(bird_rect) for pipe in self.pipes)
    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)