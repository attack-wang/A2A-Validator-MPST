from enum import Enum
class LetterState(Enum):
    CORRECT = "correct"    # green
    PRESENT = "present"    # yellow
    ABSENT = "absent"      # grey
def evaluate_guess(guess, answer):
    # returns list[LetterState] len 5
    states = [LetterState.ABSENT]*5
    remaining = Counter(answer)
    for i,(g,a) in enumerate(zip(guess, answer)):
        if g == a:
            states[i] = LetterState.CORRECT
            remaining[g] -= 1
    for i,g in enumerate(guess):
        if states[i] is LetterState.CORRECT: continue
        if remaining.get(g,0) > 0:
            states[i] = LetterState.PRESENT
            remaining[g] -= 1
    return states