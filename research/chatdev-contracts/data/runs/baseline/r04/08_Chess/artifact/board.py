class Board:
    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]
        self.setup_initial()