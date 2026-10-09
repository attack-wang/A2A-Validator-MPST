'''Data models for the crossword puzzle: directions, cells, entries and errors.'''
from enum import Enum
class Direction(Enum):
    ACROSS = "across"
    DOWN = "down"
    @classmethod
    def from_string(cls, text): ...  # parse "across"/"a"/"down"/"d"
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.solution = None  # correct letter, None for block
        self.letter = None    # currently entered letter
        self.number = None    # clue number if word starts here
        self.is_block = True  # False if usable
    def fill(self, letter)
    def clear()
    def is_correct()
    def is_empty()
    def __repr__
class Entry:  # a crossword word (across or down)
    def __init__(self, number, direction, row, col, answer, clue):
        ...
    @property length
    def cells(self) -> computed by puzzle? Or store list of cells after build.
    def is_filled()
    def is_correct()
    def pattern(self) -> current letters with '.' for empty
class CrosswordError(Exception)
class UnknownEntryError(CrosswordError)
class InvalidWordError(CrosswordError)  # conflicts with existing letters