'''
cli.py
Command-line user interface for Mastermind.
The CLI class turns raw keyboard input into validated guesses, prints the
board, feedback and banners, and asks for difficulty / replay decisions.
All player-facing text lives here so the game logic stays independent of
the presentation layer.
Input robustness: every interactive read goes through CLI._read_line(),
which converts EOFError / KeyboardInterrupt (closed or exhausted stdin,
Ctrl-D / Ctrl-Z+Enter / Ctrl-C) into QuitRoundError, so a non-interactive
run or an aborting player ends the game gracefully instead of crashing
with an uncaught traceback.
'''
from colors import BOLD, DIM, RESET
from config import COMMAND_HELP, COMMAND_QUIT
from textutils import pad
class QuitRoundError(Exception):
    """Raised when the player aborts the current round with 'quit'."""
class CLI:
    def __init__(self, palette, code_length, max_attempts, input_fn=input, output_fn=print):
        self.palette = palette
        self.code_length = code_length
        self.max_attempts = max_attempts
        self._input = input_fn
        self._print = output_fn
    # --- input robustness -----------------------------------------------
    def _read_line(self, prompt):
        """Read one line of input; treat EOF or Ctrl-C as a graceful quit.
        `input()` raises EOFError whenever stdin is exhausted or closed
        (non-interactive runs, piped input that ran out, Ctrl-D on
        Linux/macOS, Ctrl-Z+Enter on Windows) and KeyboardInterrupt on
        Ctrl-C. Both are converted into QuitRoundError so every prompt
        loop can handle an abort uniformly instead of crashing.
        """
        try:
            return self._input(prompt)
        except (EOFError, KeyboardInterrupt):
            self._print()
            raise QuitRoundError()
    # --- output helpers -------------------------------------------------
    def show_welcome(self):
        self._print()
        self._print(f"{BOLD}╔══════════════════════╗{RESET}")
        self._print(f"{BOLD}║      MASTERMIND      ║{RESET}")
        self._print(f"{BOLD}╚══════════════════════╝{RESET}")
        self._print("Crack the hidden code before you run out of attempts!")
        self._print(f"Type '{COMMAND_HELP}' to see the colors again, "
                    f"'{COMMAND_QUIT}' to abandon the round.")
    def show_legend(self):
        self._print("Colors (enter digits, letters or names):")
        self._print(f"  {self.palette.legend()}")
        self._print(f"Feedback: {BOLD}●{RESET} exact (right color, right position)  "
                    f"○ partial (right color, wrong position)")
    def show_board(self, board):
        self._print(board.render(self.palette))
    def show_feedback(self, exact, partial, attempts_remaining):
        self._print(
            f"Result: {exact} exact ●, {partial} partial ○ | "
            f"{attempts_remaining} attempt(s) remaining"
        )
    def show_secret(self, engine):
        pegs = " ".join(self.palette.get(index).peg() for index in engine.secret)
        self._print(f"The hidden code was: {pegs}")
    def show_win(self, engine):
        self._print()
        self._print(f"{BOLD}*** YOU WIN! ***{RESET}")
        self._print(f"You cracked the code in {engine.attempts_used} of "
                    f"{engine.max_attempts} attempts.")
        self.show_secret(engine)
    def show_lose(self, engine):
        self._print()
        self._print(f"{BOLD}--- YOU LOSE ---{RESET}")
        self._print(f"All {engine.max_attempts} attempts are used up.")
        self.show_secret(engine)
    def show_quit(self, engine):
        self._print()
        self._print("Round abandoned.")
        self.show_secret(engine)
    def show_error(self, message):
        self._print(f"  ✗ {message}")
    def show_goodbye(self, wins, losses):
        self._print()
        self._print(f"{BOLD}Thanks for playing Mastermind!{RESET}")
        self._print(f"Final score: {wins} win(s), {losses} loss(es).")
    # --- input helpers --------------------------------------------------
    def ask_difficulty(self, difficulties):
        """Prompt until a valid difficulty key is chosen; returns Difficulty.
        Raises QuitRoundError on EOF / Ctrl-C (via _read_line).
        """
        self._print()
        self._print(f"{BOLD}Select a difficulty:{RESET}")
        for key in sorted(difficulties):
            preset = difficulties[key]
            self._print(f"  [{key}] {preset.name:<7} - {preset.description}")
        keys = ", ".join(sorted(difficulties))
        while True:
            raw = self._read_line(f"Difficulty [{keys}]: ").strip()
            if raw in difficulties:
                return difficulties[raw]
            self.show_error(f"please enter one of: {keys}")
    def prompt_guess(self, attempt_number):
        """Ask until the player enters a parseable guess (list of indices).
        Raises QuitRoundError when 'quit' is typed or on EOF / Ctrl-C.
        """
        while True:
            raw = self._read_line(
                f"Attempt {attempt_number}/{self.max_attempts} - "
                f"enter {self.code_length} colors: "
            ).strip()
            lowered = raw.lower()
            if lowered == COMMAND_QUIT:
                raise QuitRoundError()
            if lowered == COMMAND_HELP:
                self.show_legend()
                continue
            if not raw:
                self.show_error("empty input - try again")
                continue
            guess = self.parse_guess(raw)
            if guess is None:
                self.show_error(
                    f"enter exactly {self.code_length} colors from 1-"
                    f"{self.palette.size()} (digits, letters or names), "
                    f"separated by spaces"
                )
                continue
            return guess
    def parse_guess(self, raw):
        """Convert raw text into palette indices; None when invalid."""
        tokens = raw.replace(",", " ").split()
        if len(tokens) != self.code_length:
            return None
        indices = []
        for token in tokens:
            index = self.palette.index_by_token(token)
            if index is None:
                return None
            indices.append(index)
        return indices
    def ask_play_again(self):
        """Ask what to do after a round: 'yes', 'no' or 'change' difficulty.
        Raises QuitRoundError on EOF / Ctrl-C (via _read_line).
        """
        while True:
            raw = self._read_line(
                "Play again? [y]es / [n]o / [d]ifferent difficulty: "
            ).strip().lower()
            if raw in ("y", "yes"):
                return "yes"
            if raw in ("n", "no"):
                return "no"
            if raw in ("d", "diff", "different"):
                return "change"
            self.show_error("please answer 'y', 'n' or 'd'")