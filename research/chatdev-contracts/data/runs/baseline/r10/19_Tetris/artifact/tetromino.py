def rotate(self):
    rows = len(self.matrix)
    cols = len(self.matrix[0])
    self.matrix = [[self.matrix[rows - 1 - c][r] for c in range(rows)] for r in range(cols)]