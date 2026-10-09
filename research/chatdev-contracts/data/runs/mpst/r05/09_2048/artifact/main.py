class Tile:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.prev_row = row
        self.prev_col = col
        self.is_new = False
        self.is_merged = False
        self.merged_from = []