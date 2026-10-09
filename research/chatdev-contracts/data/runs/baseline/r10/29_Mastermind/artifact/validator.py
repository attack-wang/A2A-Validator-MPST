'''
Input validation module for the Mastermind game.
Turns raw console input into a clean, validated guess, producing
human-readable error messages for anything the player submits that
is not a well-formed guess (wrong length, unknown colors, empty input).
'''
class GuessValidator:
    '''Validates raw player input against the game configuration.'''
    def __init__(self, valid_colors, code_length):
        '''
        :param valid_colors: iterable of valid single-letter color codes
        :param code_length: required number of letters per guess
        '''
        self.valid_colors = set(valid_colors)
        self.code_length = code_length
    def validate(self, raw_input):
        '''
        Validate a raw guess string.
        :param raw_input: the string exactly as typed by the player
        :return: tuple (is_valid, payload); on success payload is a list
                 of color letters, on failure it is an error message
        '''
        guess = raw_input.strip().upper().replace(" ", "")
        if not guess:
            return False, "Empty input - please type a guess (e.g. 'RGBY')."
        if len(guess) != self.code_length:
            return False, (
                f"Your guess must be exactly {self.code_length} letters long "
                f"(you typed {len(guess)})."
            )
        invalid = [ch for ch in guess if ch not in self.valid_colors]
        if invalid:
            unique_invalid = ", ".join(sorted(set(invalid)))
            return False, (
                f"Invalid color(s): {unique_invalid}. "
                f"Valid colors are: {', '.join(sorted(self.valid_colors))}."
            )
        return True, list(guess)