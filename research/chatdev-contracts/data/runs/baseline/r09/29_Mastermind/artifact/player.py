'''
player.py
Human player input handling for the Mastermind game.
Validates every guess against the expected length and the legal
color symbols, and recognizes the special quit command.
'''
import config
# Sentinel returned by get_guess when the player chooses to quit.
QUIT = 'QUIT'
class Player:
    '''Collects and validates guesses typed by the human player.'''
    def get_guess(self, code_length, valid_symbols):
        '''
        Prompt until the player enters a valid guess.
        Returns a list of color symbols, or the QUIT sentinel when the
        player types the quit command.
        '''
        example = valid_symbols[0] * code_length
        while True:
            raw = input('Enter your guess ({} symbols, e.g. "{}", or "{}" to quit): '.format(
                code_length, example, config.QUIT_COMMAND)).strip().lower()
            if raw == config.QUIT_COMMAND:
                return QUIT
            if len(raw) != code_length:
                print('  Invalid guess: it must be exactly {} symbols long.'.format(
                    code_length))
                continue
            invalid = sorted({ch for ch in raw if ch not in valid_symbols})
            if invalid:
                print('  Invalid symbol(s): {}. Allowed symbols: {}.'.format(
                    ', '.join(invalid), ', '.join(valid_symbols)))
                continue
            return list(raw)