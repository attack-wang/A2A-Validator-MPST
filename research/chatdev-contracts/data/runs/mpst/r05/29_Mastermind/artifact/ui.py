'''
ui.py
Console user interface for Mastermind.
Renders the game board, feedback pegs, prompts, and the final outcome.
Distinguishes exact matches (right color, right position) from partial
matches (right color, wrong position) using classic Mastermind pegs.
'''
import re
from config import Ansi, COLOR_ANSI
ANSI_ESCAPE_RE = re.compile(r'\033\[[0-9;]*m')
PEG_EXACT = '●'    # right color, right position ("black peg")
PEG_PARTIAL = '○'  # right color, wrong position ("white peg")
PEG_EMPTY = '·'
class ConsoleUI:
    """All console input/output for one Mastermind round."""
    def __init__(self, palette, code_length, max_attempts):
        self.palette = palette
        self.code_length = code_length
        self.max_attempts = max_attempts
    # -- low-level rendering helpers -----------------------------------------
    def _paint(self, text, *codes):
        """Wrap `text` in the given ANSI codes, resetting afterwards."""
        prefix = ''.join(codes)
        return '{}{}{}'.format(prefix, text, Ansi.RESET) if prefix else text
    def _visible_len(self, text):
        """Character count of `text` ignoring ANSI escape sequences."""
        return len(ANSI_ESCAPE_RE.sub('', text))
    def _pad(self, text, width):
        """Pad `text` to `width` visible characters (ANSI-safe)."""
        return text + ' ' * max(0, width - self._visible_len(text))
    def _render_pegs(self, feedback):
        """Render the feedback pegs (exact then partial) for one guess."""
        pegs = []
        pegs.extend(self._paint(PEG_EXACT, Ansi.WHITE) for _ in range(feedback.exact_matches))
        pegs.extend(self._paint(PEG_PARTIAL, Ansi.WHITE) for _ in range(feedback.partial_matches))
        pegs.extend(PEG_EMPTY for _ in range(self.code_length - len(pegs)))
        return ' '.join(pegs)
    def _render_guess(self, guess):
        """Render a guessed code with one ANSI color per symbol."""
        return ' '.join(self._paint(s, COLOR_ANSI.get(s, '')) for s in guess)
    # -- screens ---------------------------------------------------------------
    def show_welcome(self):
        print(self._paint('=' * 46, Ansi.CYAN))
        print(self._paint('  MASTERMIND - crack the hidden code!', Ansi.BOLD))
        print(self._paint('=' * 46, Ansi.CYAN))
    def show_rules(self):
        names = ', '.join(
            '{} ({})'.format(self._paint(s, COLOR_ANSI.get(s, '')), self.palette.name_of(s))
            for s in self.palette.symbols)
        print('\nHow to play:')
        print('  * A hidden code of {} colors has been chosen (repeats allowed).'.format(self.code_length))
        print('  * Available colors: {}'.format(names))
        print('  * Guess with letters ("RGBY") or names ("red green blue yellow").')
        print('  * {} = exact (right color & position), {} = partial (right color, wrong spot).'.format(
            PEG_EXACT, PEG_PARTIAL))
        print('  * Type "quit" to give up. You have {} attempts.\n'.format(self.max_attempts))
    def prompt_guess(self, game):
        """Ask for the next guess. Returns a symbol list, or None to give up."""
        while True:
            try:
                raw = input('Guess {} / {} ({} colors): '.format(
                    game.attempts_used + 1, self.max_attempts, self.code_length)).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if raw.lower() in ('quit', 'exit', 'q'):
                return None
            symbols = self.palette.normalize(raw)
            if symbols is None:
                print('  ! Unrecognized colors. Use letters like "RGBY" or names like "red blue".')
                continue
            if not game.is_valid_guess(symbols):
                print('  ! Guess must be exactly {} colors from: {}'.format(
                    self.code_length, ' '.join(self.palette.symbols)))
                continue
            return symbols
    def show_board(self, game):
        """Draw every guess so far together with its feedback pegs."""
        guess_width = self.code_length * 2 - 1
        peg_width = self.code_length * 2 - 1
        def rule():
            return self._paint('  ' + '-' * (4 + 3 + guess_width + 3 + peg_width + 3 + 22), Ansi.DIM)
        print()
        print(rule())
        print(self._paint('  {:<4} | {:^{gw}} | {:^{pw}}   {}'.format(
            '#', 'GUESS', 'FEEDBACK', 'DETAIL', gw=guess_width, pw=peg_width), Ansi.BOLD))
        print(rule())
        if not game.guess_history:
            print('  (no guesses yet)')
        for index, (guess, feedback) in enumerate(
                zip(game.guess_history, game.feedback_history), start=1):
            detail = '(exact {}, partial {})'.format(
                feedback.exact_matches, feedback.partial_matches)
            print('  {:<4} | {} | {}   {}'.format(
                index,
                self._pad(self._render_guess(guess), guess_width),
                self._pad(self._render_pegs(feedback), peg_width),
                detail))
        print(rule())
    def show_feedback(self, feedback):
        pegs = self._render_pegs(feedback)
        detail = 'exact: {}, partial: {}'.format(feedback.exact_matches, feedback.partial_matches)
        print('  Feedback: {}  {}'.format(pegs, self._paint(detail, Ansi.DIM)))
    def show_outcome(self, game, gave_up=False):
        print()
        secret = ' '.join(self._paint(s, COLOR_ANSI.get(s, '')) for s in game.secret)
        if gave_up:
            print('You gave up. The secret code was: {}'.format(secret))
        elif game.is_won:
            print(self._paint('You cracked the code in {} attempts - you win!'.format(
                game.attempts_used), Ansi.GREEN, Ansi.BOLD))
        else:
            print(self._paint('Out of attempts - you lose!', Ansi.RED, Ansi.BOLD))
            print('The secret code was: {}'.format(secret))