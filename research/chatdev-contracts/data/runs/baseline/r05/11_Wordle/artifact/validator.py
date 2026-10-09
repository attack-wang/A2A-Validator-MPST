'''
Input validation for player guesses.
'''
class GuessValidator:
    def __init__(self, valid_words):
        self.valid_words = {w.lower() for w in valid_words}
    def validate(self, raw):
        normalized = raw.strip().lower()
        if not normalized:
            return False, "", "Empty input — please enter a 5-letter word."
        if not normalized.isalpha():
            return False, normalized, "Only English letters A–Z are allowed."
        if len(normalized) != 5:
            return False, normalized, f"Your guess must be exactly 5 letters (got {len(normalized)})."
        if normalized not in self.valid_words:
            return False, normalized, "Not in word list."
        return True, normalized, ""