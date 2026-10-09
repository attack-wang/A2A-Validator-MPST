'''
ui.py
Console user interface for the Mastermind game.
Renders the board, feedback pegs and messages with ANSI colors when the
terminal supports them, and falls back to plain text otherwise. All
player interaction (reading guesses, replay prompts) is handled here so
the game engine stays free of I/O concerns.
'''
import os
import sys
from config import GameConfig
from feedback import Feedback
class Ansi:
    '''ANSI escape-code helpers used to colorize terminal output.'''
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    @classmethod
    def enable_windows_support(cls):
        '''Best-effort activation of ANSI codes on Windows terminals.'''
        if os.name == 'nt':
            os.system('')  # Triggers ANSI processing in the legacy console.
class ConsoleUI:
    '''Text-mode interface: draws the board and talks to the player.'''
    EXACT_PEG = '\u25cf'    # ● black peg: right color, right position
    PARTIAL_PEG = '\u25cb'  # ○ white peg: right color, wrong position
    BLANK_PEG = '\u00b7'    # · unused peg slot
    LETTER_TO_ANSI = {
        'R': Ansi.RED,
        'G': Ansi.GREEN,
        'B': Ansi.BLUE,
        'Y': Ansi.YELLOW,
        'M': Ansi.MAGENTA,
        'C': Ansi.CYAN,
    }
    def __init__(self, config: GameConfig, validator, input_stream=sys.stdin, output_stream=sys.stdout):
        self._config = config
        self._validator = validator
        self._input = input_stream
        self._output = output_stream
        self._colors_enabled = self._detect_color_support()
        Ansi.enable_windows_support()
    def _detect_color_support(self):
        '''Disable colors when NO_COLOR is set or output is not a TTY.'''
        if os.environ.get('NO_COLOR'):
            return False
        return hasattr(self._output, 'isatty') and self._output.isatty()
    def _paint(self, text, ansi):
        '''Wrap text in ANSI codes when colors are enabled and available.'''
        if self._colors_enabled and ansi:
            return f'{ansi}{text}{Ansi.RESET}'
        return text
    def _paint_peg(self, letter):
        '''Colorize a single color letter; unknown letters stay plain.'''
        return self._paint(letter, self.LETTER_TO_ANSI.get(letter))
    def _write(self, text):
        '''Write raw text and flush immediately so prompts appear in time.'''
        self._output.write(text)
        self._output.flush()
    def _writeln(self, text=''):
        '''Write one line of text followed by a newline.'''
        self._write(f'{text}\n')
    def _format_pegs(self, feedback: Feedback) -> str:
        '''Render the peg row: exact pegs, then partial pegs, then blanks.'''
        exact = self._paint(self.EXACT_PEG, Ansi.GREEN) * feedback.exact
        partial = self._paint(self.PARTIAL_PEG, Ansi.WHITE) * feedback.partial
        blanks = self.BLANK_PEG * max(0, self._config.code_length - feedback.exact - feedback.partial)
        return exact + partial + blanks
    def display_welcome(self):
        '''Show the game banner and the rules summary.'''
        self._writeln(self._paint('============ Mastermind ============', Ansi.BOLD))
        self._writeln(f'Crack the hidden code of {self._config.code_length} colors.')
        self._writeln(f'Available colors: {"".join(self._config.colors)} (duplicates possible).')
        self._writeln(f'You have {self._config.max_tries} tries. '
                      f'{self.EXACT_PEG} = exact match, {self.PARTIAL_PEG} = partial match.')
        self._writeln()
    def display_board(self, engine):
        '''Render every guess submitted so far together with its pegs.'''
        self._writeln(f'--- Board (try {engine.tries_used}/{engine.config.max_tries}) ---')
        for index, (guess, feedback) in enumerate(engine.history, start=1):
            letters = ' '.join(self._paint_peg(letter) for letter in guess)
            visible = 2 * len(guess) - 1
            padding = ' ' * max(0, 10 - visible)
            pegs = self._format_pegs(feedback)
            self._writeln(f'{index:>3}  {letters}{padding} {pegs}')
        self._writeln()
    def get_player_guess(self, engine):
        '''Prompt until the validator accepts the input; returns a guess list.
        Returns None on EOF so the caller can treat it as an abort.'''
        prompt = f'Guess #{engine.tries_used + 1}/{engine.config.max_tries}: '
        while True:
            self._write(prompt)
            raw = self._input.readline()
            if not raw:  # EOF
                return None
            raw = raw.rstrip('\n')
            guess, error = self._validator.parse(raw)
            if error is None:
                return guess
            self._writeln(self._paint(f'  [!] {error}', Ansi.RED))
    def display_feedback(self, feedback, engine):
        '''Show exact/partial counts, the peg row and remaining tries.'''
        pegs = self._format_pegs(feedback)
        self._writeln(f'Feedback: {feedback.exact} exact, {feedback.partial} partial  {pegs}')
        if not engine.is_finished:
            self._writeln(f'Tries remaining: {engine.tries_left}')
        self._writeln()
    def display_win(self, engine):
        '''Celebrate a cracked code and reveal the secret.'''
        secret = ' '.join(self._paint_peg(letter) for letter in engine.secret)
        self._writeln(self._paint(f'*** You cracked the code in {engine.tries_used} tries! ***', Ansi.GREEN))
        self._writeln(f'The secret was: {secret}')
        self._writeln()
    def display_lose(self, engine):
        '''Report defeat and reveal the secret.'''
        secret = ' '.join(self._paint_peg(letter) for letter in engine.secret)
        self._writeln(self._paint('--- Out of tries! Better luck next time. ---', Ansi.RED))
        self._writeln(f'The secret was: {secret}')
        self._writeln()
    def ask_play_again(self):
        '''Ask for a replay; returns True only on an explicit yes.'''
        self._write('Play again? [y/N]: ')
        raw = self._input.readline()
        if not raw:  # EOF
            return False
        return raw.strip().lower() in ('y', 'yes')
    def display_goodbye(self):
        '''Farewell message shown when the session ends.'''
        self._writeln('Thanks for playing Mastermind. Goodbye!')