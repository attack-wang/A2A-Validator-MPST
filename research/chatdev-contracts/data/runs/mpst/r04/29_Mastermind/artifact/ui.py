class ConsoleUI:
    def __init__(self, engine):
        self._engine = engine
    def show_welcome(self):
        legend = ', '.join(f"{letter} = {name}" for letter, name in COLORS.items())
        width = 62
        print("=" * width)
        print("M A S T E R M I N D".center(width))
        print("=" * width)
        print(f"\nA secret code of {self._engine.code_length} colors has been chosen from:")
        print(f"    {legend}")
        print(f"You have {self._engine.max_attempts} attempts to crack it.")
        print("\nFeedback pegs after each guess:")
        print("    ●  exact match   — right color, right position")
        print("    ○  partial match — right color, wrong position")
        print("\nType your guess as one word (e.g. RGBY) or spaced (R G B Y).")
        print("-" * width)
    def show_turn_banner(self):
        print(f"\nAttempt {self._engine.attempts_used + 1} "
              f"of {self._engine.max_attempts}")
    def prompt_guess(self):
        """Read one line of input; return None on EOF or Ctrl+C."""
        try:
            return input("Enter your guess > ")
        except (EOFError, KeyboardInterrupt):
            print()
            return None
    @staticmethod
    def show_error(message):
        print(f"  !! {message}")
    def show_feedback(self, feedback):
        print(f"  Feedback: {feedback}")
    def show_board(self):
        guess_width = self._engine.code_length * 2 - 1
        print("\n  #  | Guess" + " " * (guess_width - 5) + " | Feedback")
        print("  " + "-" * (4 + guess_width + 12))
        for index, (guess, feedback) in enumerate(self._engine.history, start=1):
            guess_text = ' '.join(guess)
            pegs_text = ' '.join(feedback.pegs())
            print(f"  {index:>2} | {guess_text:<{guess_width}} | {pegs_text}")