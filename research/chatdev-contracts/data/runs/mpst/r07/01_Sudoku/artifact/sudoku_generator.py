def _count_solutions(self, board, limit=2):
    empty = self._find_empty(board)
    if empty is None:
        return 1
    row, col = empty
    count = 0
    for digit in range(1, 10):
        if self._is_valid(board, row, col, digit):
            board[row][col] = digit
            count += self._count_solutions(board, limit)
            board[row][col] = self.EMPTY
            if count >= limit:
                break
    return count