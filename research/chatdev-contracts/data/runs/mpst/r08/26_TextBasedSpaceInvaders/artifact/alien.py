class Alien:
    '''A single alien belonging to the descending fleet.'''
    def __init__(self, row, col, x, y):
        self.row = row
        self.points = settings.ALIEN_POINTS_PER_ROW[row % len(settings.ALIEN_POINTS_PER_ROW)]
        self.rect = pygame.Rect(x, y, settings.ALIEN_WIDTH, settings.ALIENT_HEIGHT)
        self.color = settings.COLOR_ALIEN[row % len(settings.COLOR_ALIEN)]
        self.alive = True
        self.animation_frame = 0  # for simple animation