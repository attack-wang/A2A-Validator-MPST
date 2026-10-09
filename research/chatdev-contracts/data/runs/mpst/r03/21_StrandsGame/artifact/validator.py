'''
validator.py
Validation logic for strand merges. Decides whether a sequence of merged
strands forms one of the puzzle's target words/phrases, a real (dictionary)
word that is not a target, or an invalid formation.
'''
from word_dictionary import load_dictionary
def normalize(text):
    """Uppercase and strip spaces/hyphens/apostrophes so that phrases and
    single words can be compared fairly."""
    for ch in (" ", "-", "'", "_"):
        text = text.replace(ch, "")
    return text.upper()
class MergeValidator:
    VALID = "valid"
    REAL_WORD = "real_word"
    INVALID = "invalid"
    def __init__(self, targets, dictionary=None):
        self._targets = {}
        for target in targets:
            self._targets[normalize(target)] = target.strip().upper()
        self._dictionary = dictionary if dictionary is not None else load_dictionary()
    def is_target(self, text):
        return normalize(text) in self._targets
    def target_display(self, text):
        return self._targets[normalize(text)]
    def is_real_word(self, text):
        return normalize(text) in self._dictionary
    def validate(self, merged_text):
        """Return (status, message)."""
        key = normalize(merged_text)
        if key in self._targets:
            return self.VALID, self._targets[key]
        if key in self._dictionary:
            return self.REAL_WORD, (
                f"'{merged_text}' is a real word, but it is not one of the "
                f"words this puzzle is looking for. Keep those strands!"
            )
        return self.INVALID, (
            f"'{merged_text}' does not form a valid word or phrase. "
            f"The strands are still available - try another combination!"
        )