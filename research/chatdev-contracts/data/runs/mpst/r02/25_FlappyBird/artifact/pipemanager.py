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