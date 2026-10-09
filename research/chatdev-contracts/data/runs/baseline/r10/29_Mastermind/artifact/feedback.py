'''
Feedback module for the Mastermind game.
Implements the classic Mastermind scoring algorithm and the Feedback
value object that distinguishes between:
  * exact matches   - correct color in the correct position (black pegs)
  * partial matches - correct color in the wrong position (white pegs)
The scoring correctly handles duplicate colors by counting, for each
color, how many times it can be "paired" between the secret and the
guess, then subtracting the exact matches.
'''
from dataclasses import dataclass
from collections import Counter
@dataclass
class Feedback:
    '''Result of comparing one guess against the secret code.'''
    exact_matches: int
    partial_matches: int
    def is_win(self, code_length):
        '''Return True when every position is an exact match.'''
        return self.exact_matches == code_length
    def pegs(self, code_length):
        '''
        Render the feedback as a peg-style string.
        '●' = exact match (black peg), '○' = partial match (white peg),
        '·' = unused slot.
        '''
        return ("●" * self.exact_matches
                + "○" * self.partial_matches
                + "·" * (code_length - self.exact_matches - self.partial_matches))
    def __str__(self):
        return f"{self.exact_matches} exact, {self.partial_matches} partial"
def calculate_feedback(secret, guess):
    '''
    Compare a guess against the secret code.
    Algorithm (classic Mastermind scoring):
      1. Exact matches: count positions where secret[i] == guess[i].
      2. Color matches: for every color, take min(count in secret,
         count in guess) and sum these minima.
      3. Partial matches = total color matches - exact matches.
    :param secret: sequence of color letters (the hidden code)
    :param guess: sequence of color letters (the player's guess)
    :return: Feedback object with exact and partial match counts
    '''
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    secret_counts = Counter(secret)
    guess_counts = Counter(guess)
    total_color_matches = sum(
        min(secret_counts[color], guess_counts[color])
        for color in secret_counts
    )
    partial = total_color_matches - exact
    return Feedback(exact_matches=exact, partial_matches=partial)