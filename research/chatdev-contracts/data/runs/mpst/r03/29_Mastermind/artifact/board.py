'''
board.py
Holds the history of guesses and their feedback for the current round,
plus helpers that report how many turns have been used or remain.
'''
import config
class Board:
    '''Records every (guess, feedback) pair of the ongoing round.'''
    def __init__(self):
        self.history = []
    def reset(self):
        '''Clear the board for a new round.'''
        self.history = []
    def record(self, guess, feedback):
        '''Append one guess and its (exact, partial) feedback.'''
        self.history.append((tuple(guess), tuple(feedback)))
    @property
    def turns_used(self):
        return len(self.history)
    @property
    def turns_left(self):
        return max(0, config.MAX_TRIES - self.turns_used)
    def is_empty(self):
        return not self.history