'''
Class Clue: represents one crossword entry (an across or down word),
storing its number, direction, starting position, answer and hint text,
and exposing its length and the grid cells it covers.
'''
class Clue:
    """Represents one crossword entry (an across or down word)."""
    def __init__(self, number, direction, row, col, answer, hint):
        """
        Initialise a clue.
        Args:
            number (int): Clue number printed on the grid.
            direction (str): Either "ACROSS" or "DOWN".
            row (int): Row index of the entry's first letter.
            col (int): Column index of the entry's first letter.
            answer (str): The solution word (stored uppercase).
            hint (str): Clue text shown to the player.
        """
        self.number = number
        self.direction = direction
        self.row = row
        self.col = col
        self.answer = answer.upper()
        self.hint = hint
    @property
    def length(self):
        """int: Number of letters (squares) the entry occupies."""
        return len(self.answer)
    @property
    def cells(self):
        """list[tuple[int, int]]: Grid coordinates covered by the entry, in order."""
        step_row, step_col = (0, 1) if self.direction == "ACROSS" else (1, 0)
        return [(self.row + step_row * i, self.col + step_col * i)
                for i in range(self.length)]