def move(self, steps, board_size):
    """Move player forward and return True if they passed or landed on GO."""
    old = self.position
    self.position = (self.position + steps) % board_size
    return self.position < old  # wrapped around => passed GO