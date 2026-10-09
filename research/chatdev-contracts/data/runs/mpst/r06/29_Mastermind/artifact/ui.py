'''
ui.py
Console user interface for the Mastermind game.
`ConsoleUI` owns every interaction with the player: game-mode
selection, guess prompting and validation, history and feedback
display, win/lose messages and the replay prompt. It contains no game
logic itself; the rules live in game.py and feedback.py.
'''
import re
EXACT_PEG = "●"    # right symbol in the right position
PARTIAL_PEG = "○"  # right symbol in the wrong position
EMPTY_PEG = "·"    # symbol not matched
class ConsoleUI:
    """Text-based UI used by main.py to run Mastermind rounds."""
    def __init__(self, code_length=None):
        self._code_length = code_length
    # ---------- low-level I/O helpers ----------
    @staticmethod
    def _read_line(prompt=""):
        return input(prompt)
    @staticmethod
    def _write(text=""):
        print(text)
    # ---------- input ----------
    def prompt_mode(self, modes):
        """Ask the player to pick a game mode; returns the mode name."""
        self._write("Available game modes:")
        for index, mode in enumerate(modes, start=1):
            self._write(f"  {index}. {mode}")
        while True:
            raw = self._read_line("Select a mode (number or name): ").strip().lower()
            if raw.isdigit() and 1 <= int(raw) <= len(modes):
                return modes[int(raw) - 1]
            for mode in modes:
                if mode.lower() == raw:
                    return mode
            self._write("  Invalid choice, please try again.")
    def prompt_guess(self, attempt_number, max_attempts, symbols, code_length):
        """Prompt until the player enters a valid guess; returns list of symbols."""
        while True:
            prompt = (
                f"Attempt {attempt_number}/{max_attempts} - "
                f"Enter {code_length} symbols ({', '.join(symbols)}): "
            )
            raw = self._read_line(prompt)
            guess, error = self.parse_guess(raw, symbols, code_length)
            if error is None:
                return guess
            self._write(f"  Invalid guess: {error}")
    def parse_guess(self, raw_input, symbols, code_length):
        """Parse raw console input; returns (guess_list, None) or (None, error)."""
        # split on commas and/or whitespace
        tokens = [t for t in re.split(r"[,\s]+", raw_input.strip()) if t]
        if len(tokens) != code_length:
            return None, f"Please enter exactly {code_length} values."
        normalized = []
        for token in tokens:
            match = self._match_symbol(token, symbols)
            if match is None:
                return None, f"'{token}' is not a valid choice."
            normalized.append(match)
        return normalized, None
    def _match_symbol(self, token, symbols):
        """Case-insensitive lookup of `token` inside `symbols`."""
        lowered = token.lower()
        for symbol in symbols:
            if symbol.lower() == lowered:
                return symbol
        return None
    def prompt_replay(self):
        """Ask whether the player wants another round; returns True/False."""
        while True:
            raw = self._read_line("Play again? (y/n): ").strip().lower()
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            self._write("  Please answer 'y' (yes) or 'n' (no).")
    # ---------- output ----------
    def show_game_start(self, mode, symbols, code_length, max_attempts):
        """Print the round header with all information the player needs."""
        self._code_length = code_length
        self._write("")
        self._write("=" * 60)
        self._write(f"MASTERMIND - {mode} mode")
        self._write(f"Crack the secret code of {code_length} symbols.")
        self._write(f"Valid symbols: {', '.join(symbols)}")
        self._write(f"You have {max_attempts} attempts.")
        self._write("Feedback pegs: ● exact match, ○ partial match, · no match")
        self._write("=" * 60)
    def show_history(self, history, code_length):
        """Print every guess so far together with its feedback pegs."""
        self._write("")
        if not history:
            self._write("Guess history: (no guesses yet)")
            return
        self._write("Guess history:")
        for number, record in enumerate(history, start=1):
            guess_text = " ".join(record.guess)
            pegs = self._format_pegs(record.feedback, code_length)
            self._write(f"  {number:>2}. {guess_text:<32} {pegs}")
    def show_feedback(self, feedback, code_length):
        """Print the feedback for the most recent guess."""
        pegs = self._format_pegs(feedback, code_length)
        self._write(
            f"  Feedback: {feedback.exact_matches} exact, "
            f"{feedback.partial_matches} partial   {pegs}"
        )
    def _format_pegs(self, feedback, code_length=None):
        """Render feedback as peg characters, padded to the code length."""
        if code_length is None:
            code_length = self._code_length
        pegs = EXACT_PEG * feedback.exact_matches + PARTIAL_PEG * feedback.partial_matches
        if code_length is not None:
            pegs += EMPTY_PEG * max(0, code_length - len(pegs))
        return pegs
    def show_win(self, attempts_used, secret_code):
        """Celebrate a cracked code."""
        self._write("")
        self._write("*" * 60)
        self._write(f"CONGRATULATIONS! You cracked the code in {attempts_used} attempts!")
        self._write(f"The secret code was: {' '.join(secret_code)}")
        self._write("*" * 60)
    def show_lose(self, secret_code):
        """Reveal the code after the player runs out of attempts."""
        self._write("")
        self._write("*" * 60)
        self._write("GAME OVER - you ran out of attempts!")
        self._write(f"The secret code was: {' '.join(secret_code)}")
        self._write("*" * 60)
    def show_goodbye(self):
        """Farewell message."""
        self._write("Thanks for playing Mastermind. Goodbye!")