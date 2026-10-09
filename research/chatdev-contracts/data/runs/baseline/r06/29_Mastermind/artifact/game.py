'''
game.py
Core game engine for Mastermind.
Generates the secret code (duplicates allowed), drives the attempt
loop, scores each guess via compute_feedback, and decides the clear
win/lose outcome for the round.
'''
import random
from board import Board
from colors import active_colors, bold, letter_for
from config import EXACT_SYMBOL, PARTIAL_SYMBOL, PALETTE
from feedback import compute_feedback
class GameEngine:
    """Owns one round of Mastermind: secret, board, and attempt loop."""
    def __init__(self, code_length, palette_size, max_attempts):
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.color_names = active_colors(PALETTE, palette_size)
        self.secret = [random.choice(self.color_names) for _ in range(code_length)]
        self.board = Board(code_length, max_attempts)
    def _rules_text(self):
        """Human-readable rules reminder shown at the start of a round."""
        letters = "".join(letter_for(c) for c in self.color_names)
        return (
            f"\nGuess the hidden code of {self.code_length} colors "
            f"(palette: {', '.join(self.color_names)}).\n"
            f"Enter {self.code_length} letters ({letters}) or full color names, "
            f"separated by spaces.\n"
            f"Feedback pegs: {EXACT_SYMBOL} = right color, right position; "
            f"{PARTIAL_SYMBOL} = right color, wrong position.\n"
            f"You have {self.max_attempts} attempts. Good luck!"
        )
    def play(self, player):
        """Run the attempt loop until a win, a loss, or player exit."""
        print(self._rules_text())
        while True:
            print(self.board.render())
            guess = player.get_guess(
                self.code_length, self.board.attempts_used + 1, self.max_attempts
            )
            feedback = compute_feedback(self.secret, guess)
            self.board.add_row(guess, feedback)
            if feedback.is_perfect(self.code_length):
                print(self.board.render())
                print(bold(
                    f"\n*** YOU WIN! You cracked the code "
                    f"{self.board.render_secret(self.secret)} "
                    f"in {self.board.attempts_used} attempts. ***"
                ))
                return True
            if self.board.attempts_remaining == 0:
                print(self.board.render())
                print(bold("\n*** OUT OF ATTEMPTS - YOU LOSE. ***"))
                print(f"The secret code was: {self.board.render_secret(self.secret)}")
                return False