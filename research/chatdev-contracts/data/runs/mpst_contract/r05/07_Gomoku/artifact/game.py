SIZE = 15
EMPTY = "."
STONES = {1: "X", 2: "O"}
NAMES = {1: "Black", 2: "White"}
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class GomokuGame:
    def __init__(self, size=SIZE):
        self.size = size
        self.board = [[EMPTY] * size for _ in range(size)]
        self.current = 1

    def current_player(self):
        return self.current

    def stone(self, player):
        return STONES[player]

    def name(self, player):
        return NAMES[player]

    def switch_player(self):
        self.current = 2 if self.current == 1 else 1

    def place(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, "Move out of bounds (use 1-{}). Try again.".format(self.size)
        if self.board[row][col] != EMPTY:
            return False, "That cell is already occupied. Try again."
        self.board[row][col] = STONES[self.current]
        return True, "OK"

    def is_full(self):
        return all(cell != EMPTY for row in self.board for cell in row)

    def check_winner(self):
        for r in range(self.size):
            for c in range(self.size):
                stone = self.board[r][c]
                if stone == EMPTY:
                    continue
                for dr, dc in DIRECTIONS:
                    if self._has_five(r, c, dr, dc, stone):
                        return 1 if stone == STONES[1] else 2
        return 0

    def _has_five(self, r, c, dr, dc, stone):
        for i in range(5):
            rr, cc = r + dr * i, c + dc * i
            if not (0 <= rr < self.size and 0 <= cc < self.size):
                return False
            if self.board[rr][cc] != stone:
                return False
        return True