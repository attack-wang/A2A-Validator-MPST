class CrosswordGame:
    """State and console interaction for one crossword puzzle."""
    def __init__(self, grid, across_clues, down_clues):
        self.grid = [row.upper() for row in grid]
        self.slots, self.numbers = derive_slots(self.grid)
        self.clues = {ACROSS: across_clues, DOWN: down_clues}
        self.entries = {}          # (r, c) -> letter placed by the user
        self._validate_definition()
    # -- definition sanity checks ------------------------------------
    def _validate_definition(self):
        for direction in DIRECTIONS:
            for num, slot in self.slots[direction].items():
                if num not in self.clues[direction]:
                    raise ValueError(
                        f"Missing {direction} clue for entry {num} "
                        f"({slot['answer']}).")
        for direction in DIRECTIONS:
            for num in self.clues[direction]:
                if num not in self.slots[direction]:
                    raise ValueError(
                        f"Clue {num} {direction} has no matching word in "
                        f"the grid.")