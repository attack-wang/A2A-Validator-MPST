'''
feedback.py
Evaluates a player's guess against the secret code and produces the
classic Mastermind feedback:
  * exact matches   — right color in the right position  (black pegs)
  * partial matches — right color in the wrong position (white pegs)
A color that is already counted as an exact match is never counted
again as a partial match, and each color in the code can feed at most
one partial-match peg.
'''
from collections import Counter
from dataclasses import dataclass
@dataclass(frozen=True)
class Feedback:
    '''Immutable result of evaluating one guess against the secret code.'''
    exact: int      # right color, right position
    partial: int    # right color, wrong position
    def __str__(self):
        return f"{self.exact} exact, {self.partial} partial"
def evaluate_guess(code, guess):
    '''
    Compare a guess to the secret code.
    Args:
        code:  List of color keys representing the secret code.
        guess: List of color keys representing the player's guess.
    Returns:
        A Feedback object with the number of exact and partial matches.
    Examples:
        >>> evaluate_guess(["1", "2", "3", "4"], ["1", "2", "3", "4"]).exact
        4
        >>> evaluate_guess(["1", "2", "3", "4"], ["4", "3", "2", "1"]).partial
        4
        >>> evaluate_guess(["1", "1", "2", "3"], ["1", "1", "1", "1"]).exact
        2
        >>> evaluate_guess(["1", "1", "2", "3"], ["1", "1", "1", "1"]).partial
        0
    '''
    exact = 0
    code_remaining = Counter()
    guess_remaining = Counter()
    for code_peg, guess_peg in zip(code, guess):
        if code_peg == guess_peg:
            exact += 1
        else:
            code_remaining[code_peg] += 1
            guess_remaining[guess_peg] += 1
    # Multiset intersection: a leftover color counts as a partial match
    # only as many times as it appears in BOTH leftovers.
    partial = sum((code_remaining & guess_remaining).values())
    return Feedback(exact=exact, partial=partial)