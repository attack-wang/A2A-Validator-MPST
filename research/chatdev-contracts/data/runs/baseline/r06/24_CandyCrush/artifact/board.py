def find_matches(self):
    matched = set()
    runs = []
    for r in range(self.rows):
        start = 0
        for i in range(1, self.cols + 1):
            same = (i < self.cols and self.grid[r][i] is not None and self.grid[r][i-1] is not None
                    and self.grid[r][i].type_id == self.grid[r][i-1].type_id)
            if not same:
                length = i - start
                if length >= 3 and self.grid[r][start] is not None:
                    runs.append([(r, k) for k in range(start, i)])
                start = i
    # vertical similarly
    for col in range(self.cols):
        start = 0
        for i in range(1, self.rows + 1):
            same = (i < self.rows and self.grid[i][col] is not None and self.grid[i-1][col] is not None
                    and self.grid[i][col].type_id == self.grid[i-1][col].type_id)
            if not same:
                length = i - start
                if length >= 3 and self.grid[start][col] is not None:
                    runs.append([(k, col) for k in range(start, i)])
                start = i
    for run in runs:
        for pos in run:
            matched.add(pos)
    return matched