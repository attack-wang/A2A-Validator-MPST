'''Crossword puzzle model: builds the grid from a definition and validates entries.'''
class Puzzle:
    def __init__(self, definition):  # definition from puzzle_data
        self.title, self.width, self.height
        self.entries = [Entry(...)]
        self.grid = [[Cell...]]
        self._build_grid()
        self._assign_numbers()  # actually numbers come from data? Better: compute automatically.