'''
validator.py
Parsing and validation of the player's raw terminal input into a
well-formed guess (list of palette letters).
'''
from config import QUIT_COMMANDS
class QuitGame(Exception):
    """Raised when the player types a quit command instead of a guess."""
def parse_guess(raw_input, palette, code_length):
    """
    Parse `raw_input` into a guess.
    ...
    """
    text = (raw_input or "").strip()
    if not text:
        return None, "Empty input — please type your guess (e.g. 'R G B Y')."
    if text.lower() in QUIT_COMMANDS:
        raise QuitGame()
    tokens = text.upper().replace(",", " ").replace("-", " ").split()
    if len(tokens) == 1 and len(tokens[0]) == code_length and tokens[0].isalpha():
        tokens = list(tokens[0])
    if len(tokens) != code_length:
        return None, f"Expected {code_length} colors, got {len(tokens)}."
    guess = []
    for token in tokens:
        if len(token) != 1 or token not in palette:
            return None, f"Invalid color '{token}'. Choose from: {' '.join(palette)}."
        guess.append(token)
    return guess, None