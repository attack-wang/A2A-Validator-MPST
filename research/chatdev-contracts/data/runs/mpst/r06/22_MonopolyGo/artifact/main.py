    def ask_yes_no(self, prompt):
        """Prompt until the user answers yes or no. Returns True/False.
        Falls back to False (decline) if input is unavailable (EOF)."""
        while True:
            try:
                answer = self._input(f"{prompt} (y/n): ").strip().lower()
            except EOFError:
                self._print("[No input available — defaulting to 'no'.]")
                return False
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            self._print("Please answer 'y' or 'n'.")
    def ask_choice(self, prompt, options):
        """Prompt until the user picks one of `options` (list of keys).
        Falls back to the first option if input is unavailable (EOF)."""
        valid = [str(o).lower() for o in options]
        while True:
            try:
                answer = self._input(f"{prompt} [{'/'.join(valid)}]: ").strip().lower()
            except EOFError:
                self._print(f"[No input available — defaulting to "
                            f"'{valid[0]}'.]")
                return valid[0]
            if answer in valid:
                return answer
            self._print(f"Please choose one of: {', '.join(valid)}.")