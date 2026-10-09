'''
feedback.py
Defines the feedback model for the Wordle game.
FeedbackType is an enumeration of the three possible per-letter outcomes:
  GREEN  - the letter is correct and in the correct position
  YELLOW - the letter is present in the answer but in the wrong position
  GREY   - the letter does not appear in the answer at all
GuessFeedback stores the guess word together with the per-letter feedback
so it can be rendered on the terminal board and used for win detection.
'''
from enum import Enum
from collections import Counter
class FeedbackType(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    GREY = "grey"
class GuessFeedback:
    """Immutable result of evaluating one guess against the answer."""
    def __init__(self, guess, feedback):
        # guess: uppercase 5-letter string
        # feedback: list of FeedbackType, one per letter
        self.guess = guess
        self.feedback = list(feedback)
    @property
    def is_correct(self):
        """True when every letter is green (the guess equals the answer)."""
        return all(f == FeedbackType.GREEN for f in self.feedback)
    def __iter__(self):
        """Iterate over (letter, FeedbackType) pairs for easy rendering."""
        return iter(zip(self.guess, self.feedback))
    def __len__(self):
        return len(self.guess)
def evaluate_guess(guess, answer):
    """
    Evaluate a guess against the answer using official Wordle rules,
    correctly handling duplicated letters.
    Pass 1: mark GREEN for exact position matches and count the
            remaining (non-green) letters of the answer.
    Pass 2: for every non-green position, mark YELLOW if the letter
            still exists in the remaining counts (consuming one),
            otherwise GREY.
    """
    guess = guess.upper()
    answer = answer.upper()
    feedback = [FeedbackType.GREY] * len(guess)
    remaining = Counter(answer)
    # Pass 1: greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = FeedbackType.GREEN
            remaining[g] -= 1
    # Pass 2: yellows / greys
    for i, g in enumerate(guess):
        if feedback[i] == FeedbackType.GREEN:
            continue
        if remaining.get(g, 0) > 0:
            feedback[i] = FeedbackType.YELLOW
            remaining[g] -= 1
        else:
            feedback[i] = FeedbackType.GREY
    return GuessFeedback(guess, feedback)