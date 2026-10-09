'''Board model: grid storage, match detection, gravity, refill, shuffling.'''
import random
import config
import utils
from candy import Candy
class Board:
    def __init__(self, rows=config.ROWS, cols=config.COLS, num_types=config.NUM_CANDY_TYPES):
        """Create a rows x cols board filled with a match-free, playable layout."""
        self.rows = rows
        self.cols = cols
        self.num_types = num_types
        self.grid = [[None] * cols for _ in range(rows)]
        self._fill_initial()
    # --- setup ------------------------------------------------------------
    def _fill_initial(self):
        """Random fill that guarantees no starting matches and at least one valid move."""
        for _ in range(config.SHUFFLE_LIMIT):
            self.grid = [[None] * self.cols for _ in range(self.rows)]
            for r in range(self.rows):
                for c in range(self.cols):
                    self.grid[r][c] = Candy(self._safe_type(r, c), r, c)
            if not self.find_matches() and self.has_possible_move():
                return
        # Extremely unlikely fallback: accept last layout (shuffled below if stuck).
        self.shuffle()
    def _safe_type(self, row, col):
        """Pick a type that does not extend a horizontal/vertical run of two."""
        while True:
            t = random.randrange(self.num_types)
            if (col >= 2 and self.grid[row][col - 1] is not None
                    and self.grid[row][col - 2] is not None
                    and self.grid[row][col - 1].type_id == t
                    == self.grid[row][col - 2].type_id):
                continue
            if (row >= 2 and self.grid[row - 1][col] is not None
                    and self.grid[row - 2][col] is not None
                    and self.grid[row - 1][col].type_id == t
                    == self.grid[row - 2][col].type_id):
                continue
            return t
    # --- match detection ----------------------------------------------------
    def _runs_in_line(self, cells):
        """Return (start, end) index pairs for every run of >= 3 equal type_ids."""
        runs = []
        i, n = 0, len(cells)
        while i < n:
            if cells[i] is None:
                i += 1
                continue
            j = i + 1
            while (j < n and cells[j] is not None
                   and cells[j].type_id == cells[i].type_id):
                j += 1
            if j - i >= 3:
                runs.append((i, j))
            i = j
        return runs
    def find_match_groups(self):
        """Return a list of sets of (row, col), one per maximal matched run."""
        groups = []
        for r in range(self.rows):
            row_cells = [self.grid[r][c] for c in range(self.cols)]
            for (a, b) in self._runs_in_line(row_cells):
                groups.append({(r, c) for c in range(a, b)})
        for c in range(self.cols):
            col_cells = [self.grid[r][c] for r in range(self.rows)]
            for (a, b) in self._runs_in_line(col_cells):
                groups.append({(r, c) for r in range(a, b)})
        return groups
    def find_matches(self):
        """Return the union of all matched cells as a set of (row, col)."""
        matched = set()
        for group in self.find_match_groups():
            matched |= group
        return matched
    # --- mutation -----------------------------------------------------------
    def _swap_cells(self, a, b):
        """Swap two grid cells and keep each candy's row/col in sync."""
        (r1, c1), (r2, c2) = a, b
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
        for candy, (r, c) in ((self.grid[r1][c1], (r1, c1)),
                              (self.grid[r2][c2], (r2, c2))):
            if candy is not None:
                candy.row, candy.col = r, c
    def swap(self, a, b):
        """Swap two adjacent cells; return True if the swap creates a match.
        Invalid swaps are reverted before returning False.
        """
        (r1, c1), (r2, c2) = a, b
        if not self._are_adjacent(a, b):
            return False
        if self.grid[r1][c1] is None or self.grid[r2][c2] is None:
            return False
        self._swap_cells(a, b)
        if self.find_matches():
            return True
        self._swap_cells(a, b)  # revert: no match created
        return False
    def _are_adjacent(self, a, b):
        """True if the two cells are horizontal or vertical neighbours."""
        (r1, c1), (r2, c2) = a, b
        return abs(r1 - r2) + abs(c1 - c2) == 1
    def clear_cells(self, cells):
        """Remove candies at the given (row, col) cells (after clear animation)."""
        for r, c in cells:
            self.grid[r][c] = None
    def collapse_and_refill(self):
        """Gravity: shift candies down, spawn new ones on top; all movers start falling."""
        for c in range(self.cols):
            write = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                candy = self.grid[r][c]
                if candy is not None:
                    if r != write:
                        self.grid[write][c] = candy
                        self.grid[r][c] = None
                        candy.row, candy.col = write, c
                        candy.start_fall()  # falls from current y to the new cell
                    write -= 1
            n_new = write + 1
            for i in range(n_new):
                new_candy = Candy(random.randrange(self.num_types), i, c)
                start_y = utils.grid_to_pixel(i - n_new, c)[1]  # stack above the board
                new_candy.start_fall(initial_y=start_y)
                self.grid[i][c] = new_candy
    def all_at_rest(self):
        """True when every candy sits exactly on its grid cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                candy = self.grid[r][c]
                if candy is None or not candy.is_at_rest():
                    return False
        return True
    def has_possible_move(self):
        """True if any adjacent swap would produce a match (stuck-detection)."""
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in ((0, 1), (1, 0)):
                    r2, c2 = r + dr, c + dc
                    if r2 < self.rows and c2 < self.cols:
                        self._swap_cells((r, c), (r2, c2))
                        found = bool(self.find_matches())
                        self._swap_cells((r, c), (r2, c2))
                        if found:
                            return True
        return False
    def shuffle(self):
        """Randomly re-place existing candies until the board is playable."""
        cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        for _ in range(config.SHUFFLE_LIMIT):
            types = [self.grid[r][c].type_id for r, c in cells]
            random.shuffle(types)
            for (r, c), t in zip(cells, types):
                self.grid[r][c].type_id = t
            if not self.find_matches() and self.has_possible_move():
                return True
        return False