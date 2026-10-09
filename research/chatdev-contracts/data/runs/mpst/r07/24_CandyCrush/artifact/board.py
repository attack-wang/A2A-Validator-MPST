class Board:
    def __init__(self):
        self.grid = [[None]*COLS for _ in range(ROWS)]
        self.fill_initial()