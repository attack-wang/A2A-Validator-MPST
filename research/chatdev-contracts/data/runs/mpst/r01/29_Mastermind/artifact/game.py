'''
game.py
MastermindGame: orchestrates a full game session — builds the secret code,
runs the attempt loop, scores each guess, renders the board and reports a
clear win/lose outcome (revealing the secret when the round ends).
'''
from game_config import resolve_settings
from code_generator import generate_secret_code
from feedback import compute_feedback
from player_input import get_player_guess, QuitGame
from board import Board
from terminal_colors import colorize, BOLD, RESET
class MastermindGame:
    def __init__(self, mode, difficulty, rng=None):
        settings = resolve_settings(mode, difficulty)
        self.mode = settings["mode"]
        self.difficulty = settings["difficulty"]
        self.palette = settings["palette"]
        self.code_length = settings["code_length"]
        self.max_attempts = settings["max_attempts"]
        self.allow_duplicates = settings["allow_duplicates"]
        self.secret = generate_secret_code(
            self.palette, self.code_length,
            allow_duplicates=self.allow_duplicates, rng=rng
        )
        self.board = Board(self.palette, self.code_length, self.max_attempts)
        self.won = False
        self.attempts_used = 0
    def start(self):
        print intro
        print(self.board.render_legend())
        print rules
        try:
            for attempt in range(1, self.max_attempts + 1):
                guess = get_player_guess(self.palette, self.code_length)
                exact, partial = compute_feedback(guess, self.secret)
                self.board.add_row(guess, exact, partial)
                self.attempts_used = attempt
                print()
                print(self.board.render())
                if exact == self.code_length:
                    self.won = True
                    break
            self._finish()
        except QuitGame:
            self._abort()
    def _finish(self):
        print()
        if self.won:
            print(BOLD + f"🎉 YOU WIN! ..." + RESET)
            print(f"You broke the code in {self.attempts_used} attempt(s).")
        else:
            print(BOLD + "💀 OUT OF ATTEMPTS — YOU LOSE." + RESET)
        print("The secret code was: " + colored secret)
        print(self.board.render(secret=self.secret))  # maybe re-render with reveal