'''Board model: grid of candies, match detection, gravity, refill, shuffling.'''
import random
import config
from candy import Candy
class Board:
    """Grid of Candy objects with match detection, gravity and refill logic."""
    def __init__(self, rows=config.GRID_ROWS, cols=config.GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.grid = [[None] * cols for _ in range(rows)]
        self._fill_initial()
    # ---------------- setup helpers ---------------- #
    def _fill_initial(self):
        """Populate the grid with a match-free, movable starting layout."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = self._random_candy_avoiding_matches(r, c)
        if not self.has_possible_moves():
            self.shuffle()
    def _random_candy_avoiding_matches(self, row, col):
        """Pick a random candy type that does not complete a 3-run."""
        while True:
            t = random.randrange(config.NUM_CANDY_TYPES)
            if col >= 2 and self.grid[row][col - 1].type == t and self.grid[row][col - 2].type == t:
                continue
            if row >= 2 and self.grid[row - 1][col].type == t and self.grid[row - 2][col].type == t:
                continue
            return Candy(t, row, col)
    # ---------------- queries ---------------- #
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get(self, row, col):
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def are_adjacent(self, r1, c1, r2, c2):
        """True if the two cells are orthogonal neighbours."""
        return abs(r1 - r2) + abs(c1 - c2) == 1
    def find_matches(self):
        """Return (set of matched cells, list of groups) for runs of 3+."""
        matched = set()
        groups = []
        # horizontal runs
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                cell = self.grid[r][c]
                if cell is None:          # skip empty cells (fixes infinite loop)
                    c += 1
                    continue
                t = cell.type
                run_end = c
                while (run_end < self.cols and self.grid[r][run_end] is not None
                       and self.grid[r][run_end].type == t):
                    run_end += 1
                length = run_end - c
                if length >= 3:
                    group = [(r, cc) for cc in range(c, run_end)]
                    groups.append(group)
                    matched.update(group)
                c = run_end
        # vertical runs
        for c in range(self.cols):
            r = 0
            while r < self.rows:
                cell = self.grid[r][c]
                if cell is None:
                    r += 1
                    continue
                t = cell.type
                run_end = r
                while (run_end < self.rows and self.grid[run_end][c] is not None
                       and self.grid[run_end][c].type == t):
                    run_end += 1
                length = run_end - r
                if length >= 3:
                    group = [(rr, c) for rr in range(r, run_end)]
                    groups.append(group)
                    matched.update(group)
                r = run_end
        return matched, groups
    def has_possible_moves(self):
        """True if any adjacent swap would create a match."""
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if self.in_bounds(r2, c2):
                        if self._swap_creates_match(r, c, r2, c2):
                            return True
        return False
    def _swap_creates_match(self, r1, c1, r2, c2):
        """Temporarily swap two candy types and test for a new match."""
        a, b = self.grid[r1][c1], self.grid[r2][c2]
        if a is None or b is None:
            return False
        a.type, b.type = b.type, a.type
        matched, _ = self.find_matches()
        a.type, b.type = b.type, a.type  # revert
        return (r1, c1) in matched or (r2, c2) in matched
    def find_hint(self):
        """Return ((r1,c1),(r2,c2)) of a valid move, or None."""
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if self.in_bounds(r2, c2) and self._swap_creates_match(r, c, r2, c2):
                        return (r, c), (r2, c2)
        return None
    # ---------------- mutation ---------------- #
    def swap(self, cell_a, cell_b):
        """Swap two candies in the grid and start their swap animation."""
        r1, c1 = cell_a
        r2, c2 = cell_b
        a, b = self.grid[r1][c1], self.grid[r2][c2]
        self.grid[r1][c1], self.grid[r2][c2] = b, a
        a.start_move(r2, c2, config.SWAP_DURATION)
        b.start_move(r1, c1, config.SWAP_DURATION)
        return a, b
    def begin_clear(self, matched):
        """Mark all candies in `matched` as clearing; return the candy list."""
        clearing = []
        for r, c in matched:
            candy = self.grid[r][c]
            if candy is not None:
                candy.clearing = True
                candy.clear_timer = 0.0
                clearing.append(candy)
        return clearing
    def finish_clearing(self):
        """Remove fully-cleared candies from the grid; return True if any removed."""
        removed = False
        for r in range(self.rows):
            for c in range(self.cols):
                candy = self.grid[r][c]
                if candy is not None and candy.clearing and candy.clear_timer >= config.CLEAR_DURATION:
                    self.grid[r][c] = None
                    removed = True
        return removed
    def apply_gravity(self):
        """Compact columns downward and refill from above; return falling candies."""
        falling = []
        for c in range(self.cols):
            write_row = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                candy = self.grid[r][c]
                if candy is not None:
                    if write_row != r:
                        self.grid[write_row][c] = candy
                        self.grid[r][c] = None
                        candy.start_fall(write_row)
                        falling.append(candy)
                    write_row -= 1
            # spawn new candies above the board for the remaining empty slots
            empty_count = write_row + 1
            for target_row in range(write_row, -1, -1):
                spawn_row = target_row - empty_count
                candy = Candy(random.randrange(config.NUM_CANDY_TYPES), spawn_row, c)
                self.grid[target_row][c] = candy
                candy.start_fall(target_row)
                falling.append(candy)
        return falling
    def all_settled(self):
        """True when no candy is falling, moving or clearing."""
        for row in self.grid:
            for candy in row:
                if candy is not None and candy.is_animating():
                    return False
        return True
    def shuffle(self):
        """Shuffle types until the board is match-free and movable."""
        candies = [c for row in self.grid for c in row if c is not None]
        for _ in range(100):
            types = [candy.type for candy in candies]
            random.shuffle(types)
            idx = 0
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] is not None:
                        self.grid[r][c].type = types[idx]
                        idx += 1
            matched, _ = self.find_matches()
            if not matched and self.has_possible_moves():
                return True
        # fallback: regenerate the whole board
        self.grid = [[None] * self.cols for _ in range(self.rows)]
        self._fill_initial()
        return True