'''
Game board module for the Mastermind game.
Stores every guess the player has made together with the feedback it
received, and renders the board as readable text (including empty
slots for remaining attempts) so the player can review the full guess
history at any time.
'''
class Board:
    '''Records and renders the guess history of a Mastermind game.'''
    def __init__(self, code_length, max_attempts):
        '''
        :param code_length: number of pegs in the secret code
        :param max_attempts: total number of guesses the player may make
        '''
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.attempts = []  # list of (guess_tuple, Feedback) pairs
    def add_attempt(self, guess, feedback):
        '''Record one guess and its feedback on the board.'''
        self.attempts.append((tuple(guess), feedback))
    def is_full(self):
        '''Return True once every attempt slot has been used.'''
        return len(self.attempts) >= self.max_attempts
    def attempts_remaining(self):
        '''Return how many guesses the player still has available.'''
        return self.max_attempts - len(self.attempts)
    def render(self, colorize=None):
        '''
        Render the board as a multi-line string.
        :param colorize: optional function (letter -> styled string) used
                         to display guess letters; plain text if None
        '''
        def plain(letter):
            return letter
        paint = colorize or plain
        header = f"{'#':>2} | {'GUESS':^9} | {'FEEDBACK':^9} | MEANING"
        separator = "-" * len(header)
        lines = [header, separator]
        for idx, (guess, feedback) in enumerate(self.attempts, start=1):
            guess_str = " ".join(paint(letter) for letter in guess)
            pegs = feedback.pegs(self.code_length)
            meaning = f"{feedback.exact_matches} exact, {feedback.partial_matches} partial"
            lines.append(f"{idx:>2} | {guess_str:^9} | {pegs:^9} | {meaning}")
        for idx in range(len(self.attempts) + 1, self.max_attempts + 1):
            empty = " ".join("·" for _ in range(self.code_length))
            lines.append(f"{idx:>2} | {empty:^9} | {'·' * self.code_length:^9} |")
        lines.append(separator)
        lines.append(f"Attempts used: {len(self.attempts)}/{self.max_attempts} "
                     f"(remaining: {self.attempts_remaining()})")
        return "\n".join(lines)