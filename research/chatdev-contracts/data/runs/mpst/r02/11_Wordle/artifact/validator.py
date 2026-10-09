'''
validator.py
Validation of raw user input before it is accepted as a guess.
'''
import re
_WORD_RE = re.compile(r"^[a-z]+$")
def validate_guess(raw_input, valid_words, word_length=5):
    """Validate the raw terminal input.
    Returns (is_valid, cleaned_word_or_None, error_message_or_None).
    """
    guess = raw_input.strip().lower()
    if not guess:
        return False, None, "Please enter a word."
    if len(guess) != word_length:
        return False, None, f"Your guess must be exactly {word_length} letters long (got {len(guess)})."
    if not _WORD_RE.match(guess):
        return False, None, "Only English letters (a-z) are allowed."
    if guess not in valid_words:
        return False, None, f"'{guess}' is not in the word list."
    return True, guess, None