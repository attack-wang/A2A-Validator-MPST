'''
feedback.py
Implements the standard Wordle feedback rules: for every letter of a
guess, decide whether it is CORRECT (green), PRESENT but misplaced
(yellow) or ABSENT (grey), correctly handling repeated letters.
'''
from collections import Counter
from enum import Enum
import colors
class LetterState(Enum):
    '''Possible per-letter feedback states.'''
    CORRECT = "correct"   # right letter, right position  -> green
    PRESENT = "present"   # right letter, wrong position   -> yellow
    ABSENT = "absent"     # letter not in the answer       -> grey
def evaluate_guess(guess, answer):
    '''
    Compare `guess` with `answer` (both 5-letter lowercase strings) and
    return a list of LetterState, one per position.
    Standard Wordle duplicate handling:
      1. Greens are assigned first and consume letters from the answer.
      2. Remaining letters are matched for yellows, consuming counts.
      3. Anything left over is grey.
    '''
    if len(guess) != len(answer):
        raise ValueError("guess and answer must have the same length")
    states = [LetterState.ABSENT] * len(guess)
    remaining = Counter(answer)
    # First pass: greens.
    for i, (g_char, a_char) in enumerate(zip(guess, answer)):
        if g_char == a_char:
            states[i] = LetterState.CORRECT
            remaining[g_char] -= 1
    # Second pass: yellows within the remaining letter budget.
    for i, g_char in enumerate(guess):
        if states[i] == LetterState.CORRECT:
            continue
        if remaining.get(g_char, 0) > 0:
            states[i] = LetterState.PRESENT
            remaining[g_char] -= 1
    return states
def state_color(state):
    '''Map a LetterState to its ANSI color constant.'''
    return {
        LetterState.CORRECT: colors.GREEN,
        LetterState.PRESENT: colors.YELLOW,
        LetterState.ABSENT: colors.GREY,
    }[state]
def render_guess_row(guess, states):
    '''
    Render one guess as a colored board row, e.g.
        │ G │ R │ E │ A │ T │
    with each letter painted according to its feedback state.
    '''
    cells = []
    for letter, state in zip(guess, states):
        cells.append(colors.colorize(letter.upper(), state_color(state)))
    return "│ " + " │ ".join(cells) + " │"
def render_empty_row(word_length=5):
    '''Render a placeholder row for attempts not used yet.'''
    cells = [" " for _ in range(word_length)]
    return "│ " + " │ ".join(cells) + " │"