'''
Spawns, moves, and recycles pipe pairs with score-based difficulty.
'''
import random
import settings
from pipe import PipePair
class PipeManager:
    def __init__(self):
        self.pipes = []
        self.reset()
    def reset(self):
        self.pipes.clear()
    def gap_for(self, score):
        max_gap = max(settings.MIN_GAP, settings.BASE_GAP - score * settings.GAP_SHRINK)
        min_gap = max(settings.MIN_GAP, int(max_gap * 0.85))
        return random.randint(min_gap, int(max_gap))
    def speed_for(self, score):
        return min(settings.MAX_SPEED, settings.BASE_SPEED + score * settings.SPEED_INCREMENT)
    def _spawn(self, score):
        gap_size = self.gap_for(score)
        margin = gap_size / 2 + settings.PIPE_OVERHANG + 10
        gap_center = random.uniform(margin, settings.GROUND_Y - margin)
        if self.pipes:
            x = self.pipes[-1].x + settings.PIPE_SPACING
        else:
            x = settings.WIDTH + 100
        self.pipes.append(PipePair(x, gap_center, gap_size, self.speed_for(score)))
    def update(self, dt, score):
        if not self.pipes:
            self._spawn(score)
        while self.pipes[-1].x <= settings.WIDTH - settings.PIPE_SPACING:
            self._spawn(score)
        speed = self.speed_for(score)
        for pipe in self.pipes:
            pipe.update(dt, speed)
        self.pipes = [p for p in self.pipes if not p.off_screen()]
    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)