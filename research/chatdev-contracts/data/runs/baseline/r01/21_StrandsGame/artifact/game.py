'''
game.py - Game orchestration: puzzle selection, input loop, merge
validation calls, and completion confirmation.
'''
from puzzle import (Puzzle, MergeResult,
                    ERR_RANGE, ERR_DUPLICATE, ERR_USED,
                    ERR_EMPTY, ERR_INVALID)
import ui
class StrandsGame:
    """Top-level controller: owns puzzles and runs the interactive loop."""
    def __init__(self, puzzles_data):
        self.puzzles_data = puzzles_data
        self.puzzle = None
    # ---- setup ----
    def select_puzzle(self):
        """Let the player choose a puzzle from the available list."""
        ui.print_puzzle_menu(self.puzzles_data)
        while True:
            raw = input("Choose a puzzle number: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(self.puzzles_data):
                data = self.puzzles_data[int(raw) - 1]
                self.puzzle = Puzzle(data["title"], data["theme"], data["entries"])
                return
            ui.print_error("Please enter a valid puzzle number.")
    # ---- main loop ----
    def run(self):
        """Main loop: render → read input → merge → feedback → completion."""
        ui.print_banner()
        self.select_puzzle()
        ui.print_help()
        input("\nPress Enter to begin...")
        last_feedback = None
        while not self.puzzle.is_complete():
            ui.clear_screen()
            ui.render_puzzle(self.puzzle)
            if last_feedback is not None:
                ui.print_feedback(last_feedback)
            last_feedback = None
            raw = input("\nEnter strand numbers (e.g. 1 3 5), or h/?/q: ").strip()
            if raw.lower() in ("q", "quit"):
                ui.print_quit_message(self.puzzle)
                return
            if raw.lower() in ("h", "hint"):
                last_feedback = self._give_hint()
                continue
            if raw.lower() in ("?", "help"):
                ui.print_help()
                input("\nPress Enter to continue...")
                continue
            numbers = self._parse_numbers(raw)
            if numbers is None:
                last_feedback = MergeResult(False, ERR_INVALID,
                                            message="Enter strand numbers only (e.g. 1 3 5).")
                continue
            last_feedback = self.puzzle.attempt_merge(numbers)
        ui.clear_screen()
        ui.render_puzzle(self.puzzle)
        if last_feedback is not None:
            ui.print_feedback(last_feedback)
        ui.print_completion(self.puzzle, self.puzzle.get_stats())
    # ---- helpers ----
    def _parse_numbers(self, raw):
        """Parse space-separated integers; return None on bad input."""
        try:
            return [int(tok) for tok in raw.split()]
        except ValueError:
            return None
    def _give_hint(self):
        """Reveal one strand belonging to an unfound word; return feedback."""
        number = self.puzzle.reveal_hint()
        if number is None:
            return MergeResult(False, "HINT_EXHAUSTED",
                               message="No hints left — every remaining strand is already revealed.")
        return MergeResult(False, "HINT",
                           message=f"Hint: strand {number} is part of an unfound word.")