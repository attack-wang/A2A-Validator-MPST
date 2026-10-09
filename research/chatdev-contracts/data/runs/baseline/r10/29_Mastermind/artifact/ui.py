'''
Console user-interface module for the Mastermind game.
Implements ConsoleUI, which owns all printing and input handling:
welcome/rules screens, board rendering, guess prompting (with 'Q' to
quit), feedback display, win/lose messages, and replay prompting.
All input reads are guarded against stream exhaustion (EOFError) and
keyboard interrupts so the program always terminates gracefully
instead of crashing with a traceback on non-interactive runs.
'''
class QuitGame(Exception):
    '''Raised when the player chooses to quit the current game.'''
class ConsoleUI:
    '''Text-based user interface for the Mastermind game.'''
    def __init__(self, config):
        '''
        :param config: GameConfig providing code length, palette, attempts
        '''
        self.config = config
    # ------------------------------------------------------------------
    # Safe input helper (fix for the EOFError crash reported in testing)
    # ------------------------------------------------------------------
    @staticmethod
    def _read_line(prompt):
        '''
        Read one line of input safely.
        Converts stream exhaustion (EOFError) and keyboard interrupts
        (KeyboardInterrupt) into a QuitGame signal so the main loop can
        shut down gracefully instead of propagating an uncaught crash.
        '''
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            raise QuitGame
    def show_welcome(self):
        '''Print the game banner.'''
        print("=" * 50)
        print("WELCOME TO MASTERMIND".center(50))
        print("=" * 50)
    def show_rules(self):
        '''Explain the rules and feedback symbols before each game.'''
        print(f"\nI have chosen a secret code of {self.config.code_length} colors.")
        print(f"Available colors: {self.config.valid_letters_str}")
        print(f"You have {self.config.max_attempts} attempts to crack it.")
        print("Feedback after each guess:")
        print("  ● = exact match (right color, right position)")
        print("  ○ = partial match (right color, wrong position)")
        print("Enter guesses as letters, e.g. 'RGBY'. Type 'Q' to quit.\n")
    def show_board(self, board):
        '''Render and print the current board state.'''
        print(board.render())
    def prompt_guess(self, validator, attempt_number):
        '''
        Keep asking until the player submits a valid guess.
        :return: list of validated color letters
        :raises QuitGame: if the player types Q/QUIT/EXIT, or the input
                          stream is exhausted or interrupted
        '''
        while True:
            raw = self._read_line(
                f"Attempt {attempt_number}/{self.config.max_attempts}> "
            )
            if raw.strip().upper() in ("Q", "QUIT", "EXIT"):
                raise QuitGame
            is_valid, payload = validator.validate(raw)
            if is_valid:
                return payload
            print(f"  Invalid guess: {payload}")
    def show_feedback(self, feedback):
        '''Print the feedback line for the last guess.'''
        print(f"  Result: {feedback}\n")
    def show_win(self, secret, attempts_used):
        '''Print the victory message, revealing the code.'''
        print("\n*** CONGRATULATIONS! You cracked the code in "
              f"{attempts_used} attempt(s): {' '.join(secret)} ***")
    def show_lose(self, secret):
        '''Print the defeat message, revealing the code.'''
        print(f"\n--- Out of attempts! The secret code was: {' '.join(secret)} ---")
    def ask_replay(self):
        '''
        Ask whether to start a new game. Return True to replay.
        On EOF or keyboard interrupt, return False so the replay loop
        exits gracefully through show_goodbye() with a clean status.
        '''
        try:
            return input("\nPlay again? (y/n): ").strip().lower() in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            return False
    def show_goodbye(self):
        '''Print the farewell message.'''
        print("Thanks for playing Mastermind. Goodbye!")