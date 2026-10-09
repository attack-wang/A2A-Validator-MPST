ROWS = 6
COLS = 7


class ConnectFour:
    def __init__(self):
        self.board = [[' '] * COLS for _ in range(ROWS)]
        self.current = 'X'

    def display(self):
        print()
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('+' + '-+' * COLS)
        print(' 1 2 3 4 5 6 7')

    def drop(self, col):
        """Place the current player's disc in the column; return row index or None."""
        if not 0 <= col < COLS:
            return None
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current
                return row
        return None

    def is_win(self, row, col):
        """Check whether the disc at (row, col) completes a line of four."""
        player = self.board[row][col]
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            count = 1
            for step in (1, -1):
                r, c = row + dr * step, col + dc * step
                while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                    count += 1
                    r += dr * step
                    c += dc * step
            if count >= 4:
                return True
        return False

    def is_full(self):
        return all(self.board[0][c] != ' ' for c in range(COLS))

    def switch(self):
        self.current = 'O' if self.current == 'X' else 'X'