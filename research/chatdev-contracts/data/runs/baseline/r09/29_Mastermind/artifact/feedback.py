'''
feedback.py
Scoring logic for Mastermind guesses.
Given the secret code and a player's guess, this module computes
the two-part Mastermind feedback:
  * exact matches   -- pegs with the right color in the right position
  * partial matches -- pegs with a color that exists elsewhere in the
                       code but is currently in the wrong position
The algorithm is the standard two-pass approach: first count exact
matches and remove them from both sequences, then count how many
colors overlap (per color, capped by availability) in what remains.
This correctly handles duplicated colors in either sequence.
'''
from collections import Counter
from dataclasses import dataclass
@dataclass
class Feedback:
    '''Structured result of scoring one guess against the secret code.'''
    exact: int    # right color, right position ("black pegs")
    partial: int  # right color, wrong position ("white pegs")
    @property
    def is_solved(self):
        '''True when every position matches exactly (the code is cracked).'''
        return self.exact == ... 