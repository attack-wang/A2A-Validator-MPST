'''
validator.py
Parses and validates raw keyboard input from the player.
Accepts flexible formats such as "1234", "1 2 3 4", "R,G,B,Y" or
"rgby" and converts them into a normalized list of color keys
(digits "1".."6"). Invalid input yields a human-readable error
message instead of raising an exception.
'''
from constants import COLORS, LETTER_TO_KEY
IGNORED_CHARACTERS = (" ", ",", "-", "_", ".")
def normalize_guess(raw_input, code_length):
    '''
    Turn raw player input into a validated list of color keys.
    Args:
        raw_input:   The string typed by the player.
        code_length: Required number of pegs in the guess.
    Returns:
        (guess, None) on success, where guess is a list of color keys;
        (None, error_message) on failure.
    '''
    cleaned = raw_input.strip()
    for character in IGNORED_CHARACTERS:
        cleaned = cleaned.replace(character, "")
    if not cleaned:
        return None, "Empty input — please enter {0} colors (e.g. '1234').".format(code_length)
    if len(cleaned) != code_length:
        return None, (
            "Your guess must contain exactly {0} colors, "
            "but you entered {1} ('{2}').".format(code_length, len(cleaned), raw_input.strip())
        )
    guess = []
    for character in cleaned:
        key = character if character in COLORS else LETTER_TO_KEY.get(character.lower())
        if key is None:
            return None, "'{0}' is not a valid color. Valid entries: 1-6 or R G B Y O P.".format(character)
        guess.append(key)
    return guess, None