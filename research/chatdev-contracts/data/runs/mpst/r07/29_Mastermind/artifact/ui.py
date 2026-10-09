'''
ui.py
Console front end for the Mastermind game.
ConsoleUI renders the welcome banner, the palette legend, the guess
history with feedback pegs, and the final win/lose screens. It also
owns all input prompts and error messages. All game rules live in
game_engine.py; this module only formats and asks.
'''
import sys
from validator import GuessError, parse_guess
class ConsoleUI:
    '''Text-based user interface for Mastermind.'''
    def __init__(self, config, input_stream=None, output_stream=None):
        '''
        Args:
            config: GameConfig instance.
            input_stream: source for player input (default: stdin).
            output_stream: sink for all output (default: stdout).
        '''
        self.config = config
        self.input_stream = input_stream if input_stream is not None else sys.stdin
        self.output_stream = output_stream if output_stream is not None else sys.stdout
    # ------------------------------------------------------------------
    # low-level helpers
    # ------------------------------------------------------------------
    def _write(self, text=''):
        '''Print a line to the output stream.'''
        print(text, file=self.output_stream)
    def _read(self, prompt):
        '''Show a prompt and return the stripped line from the input stream.'''
        self.output_stream.write(prompt)
        self.output_stream.flush()
        line = self.input_stream.readline()
        if line == '':  # EOF (e.g. Ctrl-D / piped input exhausted)
            raise EOFError('Input stream closed.')
        return line.strip()
    # ------------------------------------------------------------------
    # screens
    # ------------------------------------------------------------------
    def show_welcome(self):
        '''Print the banner, the rules and the palette legend.'''
        self._write('=' * 60)
        self._write('            M A S T E R M I N D')
        self._write('=' * 60)
        self._write('I have hidden a code of %d colors.' % self.config.code_length)
        if self.config.allow_duplicates:
            self._write('Colors may repeat within the code!')
        else:
            self._write('Every color appears at most once in the code.')
        self._write('You have %d attempts to crack it.' % self.config.max_attempts)
        self._write('')
        self._write('Available colors: %s' % self.config.color_key)
        self._write('')
        self._write('After every guess you get feedback pegs:')
        self._write('  %s = right color in the right position (exact match)'
                    % self.config.exact_peg)
        self._write('  %s = right color in the wrong position (partial match)'
                    % self.config.partial_peg)
        self._write('  %s = color not in the code (or already accounted for)'
                    % self.config.miss_peg)
        self._write('')
        self._write('Type your guess as %d characters, e.g. %s -- spaces or'
                    ' commas are fine too.'
                    % (self.config.code_length,
                       ' '.join(self.config.colors[:self.config.code_length])))
        self._write('=' * 60)
    # ------------------------------------------------------------------
    # prompts
    # ------------------------------------------------------------------
    def prompt_guess(self, attempt_number):
        '''
        Ask the player for a guess until the input parses cleanly.
        Args:
            attempt_number: 1-based number of the attempt being played.
        Returns:
            List of normalized color tokens for the guess.
        Raises:
            EOFError: when the input stream is closed (handled by caller).
        '''
        while True:
            try:
                raw = self._read(
                    '\nAttempt %d/%d -- enter your guess: '
                    % (attempt_number, self.config.max_attempts))
                return parse_guess(raw, self.config)
            except GuessError as exc:
                self.show_error(str(exc))
    def ask_play_again(self):
        '''
        Ask whether the player wants another round.
        Returns:
            True for yes, False for no (EOF is treated as "no").
        '''
        while True:
            try:
                raw = self._read('\nPlay again? (y/n): ').lower()
            except EOFError:
                return False
            if raw in ('y', 'yes'):
                return True
            if raw in ('n', 'no'):
                return False
            self.show_error("Please answer 'y' or 'n'.")
    # ------------------------------------------------------------------
    # feedback and outcome screens
    # ------------------------------------------------------------------
    def show_error(self, message):
        '''Print a player-facing error message.'''
        self._write('!! %s' % message)
    def show_attempts_left(self, remaining):
        '''Show how many guesses the player still has.'''
        self._write('Attempts remaining: %d' % remaining)
    def show_guess_result(self, guess, feedback):
        '''Render one guess together with its feedback pegs.'''
        self._write('  %s  ->  %s' % (
            ' '.join(guess),
            feedback.describe(self.config.exact_peg,
                              self.config.partial_peg,
                              self.config.miss_peg)))
    def show_win(self, attempts_used):
        '''Celebrate a cracked code with a clear win outcome.'''
        self._write('=' * 60)
        self._write('CONGRATULATIONS! You cracked the code in %d guess(es).'
                    % attempts_used)
        self._write('=' * 60)
    def show_lose(self, secret):
        '''Reveal the hidden code with a clear lose outcome.'''
        self._write('=' * 60)
        self._write('Sorry, you are out of attempts. The hidden code was: %s'
                    % ' '.join(secret))
        self._write('=' * 60)
    def show_goodbye(self):
        '''Farewell message when the player quits.'''
        self._write('Thanks for playing Mastermind. Goodbye!')