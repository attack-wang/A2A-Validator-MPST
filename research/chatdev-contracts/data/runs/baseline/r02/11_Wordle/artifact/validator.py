'''
validator.py
Validates raw user input before it is evaluated against the answer.
'''
class GuessValidator:
    WORD_LENGTH = 5
    def validate(self, raw):
        guess = raw.strip().lower()
        if not guess:
            return False, "Empty input..."
        if len(guess) != 5:
            return False, f"..."
        if not guess.isalpha():
            return False, "..."
        return True, guess