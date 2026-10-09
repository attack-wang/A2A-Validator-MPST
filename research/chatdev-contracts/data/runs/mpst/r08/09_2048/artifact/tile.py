class Tile:
    def __init__(self, row, col, value, is_new=False):
        self.row = row
        self.col = col
        self.value = value
        self.is_new = is_new
        self.previous_row = row
        self.previous_col = col
        self.merged_from = None