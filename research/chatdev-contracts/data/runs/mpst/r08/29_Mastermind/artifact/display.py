'''
display.py
All terminal rendering for the Mastermind game: welcome banner,
colored codes, feedback pegs, guess history, win/lose messages and
the goodbye sign-off. Unicode pegs are used when the console
supports them, with automatic ASCII fallbacks otherwise.
'''
import os
import sys
import config
def enable_ansi_support():
    '''Best-effort activation of ANSI escape codes (needed on Windows).'''
    if os.name == 'nt':
        os.system('')  # Enables VT processing in Windows 10+ consoles.
class Display:
    '''Draws every screen the player sees during a game.'''
    WIDTH = 58
    def __init__(self):
        self.unicode_ok = self._check_unicode()
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _check_unicode(self):
        '''Return True if stdout can encode every Unicode peg symbol.'''
        try:
            (config.BLACK_PEG + config.WHITE_PEG + config.EMPTY_PEG).encode(
                sys.stdout.encoding or 'ascii')
            return True
        except (UnicodeEncodeError, AttributeError):
            return False
    def _peg(self, unicode_symbol, ascii_symbol):
        return unicode_symbol if self.unicode_ok else ascii_symbol
    def _format_pegs(self, exact, partial, code_length):
        '''Render the feedback pegs for one guess.'''
        black = self._peg(config.BLACK_PEG, config.ASCII_BLACK_PEG)
        white = self._peg(config.WHITE_PEG, config.ASCII_WHITE_PEG)
        empty = self._peg(config.EMPTY_PEG, config.ASCII_EMPTY_PEG)
        pegs = ([black] * exact + [white] * partial +
                [empty] * max(0, code_length - exact - partial))
        return ' '.join(pegs)
    def _format_code(self, code):
        '''Render a color code, painted with ANSI colors when possible.'''
        try:
            is_tty = sys.stdout.isatty()
        except AttributeError:
            is_tty = False
        if not is_tty:
            return ' '.join(code)
        painted = []
        for color in code:
            ansi = config.ANSI_COLORS.get(color)
            if ansi:
                painted.append('{}{}{}'.format(ansi, color, config.ANSI_RESET))
            else:
                painted.append(color)
        return ' '.join(painted)
    def _rule(self, char='-'):
        return char * self.WIDTH
    # ------------------------------------------------------------------
    # Public screens
    # ------------------------------------------------------------------
    def show_welcome(self, code_length, max_attempts, allow_duplicates):
        print('=' * self.WIDTH)
        print('           W E L C O M E   T O   M A S T E R M I N D')
        print('=' * self.WIDTH)
        print('Crack the hidden code!')
        print('Rules:')
        print('  * The computer has hidden a code of {} colors.'.format(code_length))
        if allow_duplicates:
            print('  * Colors may repeat in the code.')
        else:
            print('  * Every color appears at most once in the code.')
        print('  * You have {} attempts to guess it.'.format(max_attempts))
        print('  * After each guess you get pegs:')
        print('      {} = exact match   (right color, right position)'.format(
            self._peg(config.BLACK_PEG, config.ASCII_BLACK_PEG)))
        print('      {} = partial match (right color, wrong position)'.format(
            self._peg(config.WHITE_PEG, config.ASCII_WHITE_PEG)))
        print('Available colors:')
        print('  ' + ', '.join('{} = {}'.format(code, name)
                               for code, name in config.COLOR_NAMES.items()))
        print("Type 'help' during the game to see input examples, "
              "or 'quit' to exit.")
        print('=' * self.WIDTH)
    def show_feedback(self, exact, partial, code_length):
        print('>> Feedback: {}  ->  {} exact, {} partial'.format(
            self._format_pegs(exact, partial, code_length), exact, partial))
    def show_history(self, history, max_attempts):
        print('=' * self.WIDTH)
        print('   GUESS        FEEDBACK')
        print('-' * self.WIDTH)
        for i, (guess, exact, partial) in enumerate(history, start=1):
            plain = ' '.join(guess)
            colored = self._format_code(guess)
            pad = ' ' * max(0, 12 - len(plain))
            print('  {}. {}{}  {}   ({} exact, {} partial)'.format(
                i, colored, pad, self._format_pegs(exact, partial, len(guess)),
                exact, partial))
        print('-' * self.WIDTH)
        print('  Attempts used: {}/{}'.format(len(history), max_attempts))
        print('=' * self.WIDTH)
    def show_win(self, attempts_used, max_attempts, secret):
        print()
        print('*** CONGRATULATIONS! You cracked the code in {} of {} attempts! ***'.format(attempts_used, max_attempts))
        print('The secret code was: {}'.format(self._format_code(secret)))
    def show_lose(self, secret):
        print()
        print('*** GAME OVER - you ran out of attempts. ***')
        print('The secret code was: {}'.format(self._format_code(secret)))
    def show_quit(self, secret):
        print()
        print('You gave up. The secret code was: {}'.format(self._format_code(secret)))
    def show_help(self, code_length):
        print('-' * self.WIDTH)
        print('How to enter a guess:')
        print('  * Separate {} colors with spaces, e.g.: R G B Y'.format(code_length))
        print('  * Commas or dashes also work: R,G,B,Y or R-G-B-Y')
        print('  * One compact token works too: RGBY')
        print('  * Available colors: {}'.format(' '.join(config.AVAILABLE_COLORS)))
        print("  * Type 'quit' to abandon the game.")
        print('-' * self.WIDTH)
    def show_goodbye(self):
        print()
        print('Thanks for playing Mastermind. Goodbye!')