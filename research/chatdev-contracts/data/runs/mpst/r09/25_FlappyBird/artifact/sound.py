def __init__(self):
    self.pipes = []
    self.reset()
def reset(self):
    self.pipes.clear()
    self.next_spawn_x = settings.WIDTH + 100
def _spawn(self, score):
    ...
    self.pipes.append(PipePair(self.next_spawn_x, gap_center, gap_size, speed))
def update(self, dt, score):
    if not self.pipes:
        self._spawn(score)
    while self.pipes[-1].x <= settings.WIDTH - settings.PIPE_SPACING:
        self._spawn(score)