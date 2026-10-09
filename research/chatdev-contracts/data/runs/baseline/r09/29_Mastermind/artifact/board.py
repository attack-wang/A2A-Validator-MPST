'''
board.py
Text rendering of the Mastermind game board.
The Board keeps the history of guesses and their feedback and knows
how to print the welcome screen, the rules, the running scoreboard,
and the final win/lose banner.
'''
from colors import COLORS, EXACT_PEG, PARTIAL_PEG, EMPTY_PEG, describe_code
import config
class Board:
    '''Responsible for all textual presentation of the game state.'''
    def __init__(self):
        self.attempts = []  # list of (guess, Feedback) tuples
    def add_attempt(self, guess, feedback):
        '''Record one guess and its feedback in the history.'''
        self.attempts.append((list(guess), feedback))
    def render_welcome(self):
        '''Print the welcome banner and the color legend.'''
        ...
    def render_rules(self):
        '''Print the rules / help text.'''
        ...
    def render(self):
        '''Print the scoreboard with every attempt so far.'''
        ...
    def render_win(self, tries_used):
        '''Print the victory banner.'''
        ...
    def render_lose(self, secret_code):
        '''Print the game-over banner and reveal the code.'''
        ...