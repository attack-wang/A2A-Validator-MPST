'''
cli.py
Console user interface for the trivia quiz. Handles all printing and
input collection so the quiz engine stays independent of I/O details.
Classes:
    ConsoleUI: Command-line interface used by the Quiz engine.
'''
from question import ShortAnswerQuestion
class ConsoleUI:
    """Command-line interface used by the Quiz engine."""
    QUIT_COMMANDS = {"q", "quit", "exit"}
    def show_message(self, text=""):
        """Print a message followed by a newline."""
        print(text)
    def show_intro(self, total_questions):
        """Print the quiz banner and instructions."""
        line = "=" * 60
        self.show_message(line)
        self.show_message("        WELCOME TO THE TRIVIA QUIZ")
        self.show_message(line)
        self.show_message(f"You will be asked {total_questions} question(s).")
        self.show_message("Multiple-choice: reply with the letter (e.g. B) or the choice text.")
        self.show_message("Short-answer  : reply with free text (spelling matters, case does not).")
        self.show_message("Type 'q' at any prompt to quit early.")
        self.show_message(line)
    def prompt_answer(self, question):
        """Prompt the user for an answer; returns None if the user quits."""
        if isinstance(question, ShortAnswerQuestion):
            hint = "short answer"
        else:
            hint = "letter or choice text"
        while True:
            try:
                raw = input(f"Your answer ({hint}): ").strip()
            except (EOFError, KeyboardInterrupt):
                self.show_message()
                return None
            if raw.lower() in self.QUIT_COMMANDS:
                return None
            if raw:
                return raw
            self.show_message("Please type something (or 'q' to quit).")
    def confirm(self, prompt, default=False):
        """Ask a yes/no question; returns True for yes, False for no."""
        suffix = "[Y/n]" if default else "[y/N]"
        try:
            raw = input(f"{prompt} {suffix}: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            self.show_message()
            return default
        if not raw:
            return default
        return raw in ("y", "yes")
    def prompt_index(self, prompt, count):
        """Ask the user to pick a number between 1 and count (inclusive).
        Returns the chosen number, or None if the user quits via
        EOF (Ctrl+D) or Ctrl+C — consistent with prompt_answer().
        """
        while True:
            try:
                raw = input(f"{prompt} [1-{count}]: ").strip()
            except (EOFError, KeyboardInterrupt):
                self.show_message()
                return None
            if raw.lower() in self.QUIT_COMMANDS:
                return None
            if raw.isdigit() and 1 <= int(raw) <= count:
                return int(raw)
            self.show_message(f"Please enter a number between 1 and {count} (or 'q' to quit).")