class CrosswordPuzzle:
    """Holds the puzzle state and implements the game logic."""
    def __init__(self, solution_grid, entries):
        self.solution = [row[:] for row in solution_grid]  # deep copy
        self.entries = entries
        self.rows = len(solution_grid)
        self.cols = len(solution_grid[0]) if self.rows else 0
        # Player's current grid: blocked squares '#', unfilled open squares None
        self.grid = [[cell if cell == '#' else None for cell in row]
                     for row in self.solution]
        # Index entries by (number, direction) for quick lookup
        self.lookup = {(num, direction): entry
                       for num, direction, *_ in ...}