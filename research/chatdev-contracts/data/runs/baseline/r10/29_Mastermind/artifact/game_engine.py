'''
Game engine module for the Mastermind game.
Orchestrates a full game session: generating the secret code, accepting
guesses, computing feedback, tracking the board state, and determining
the win/lose outcome.
'''
from code_generator import CodeGenerator
from feedback import calculate_feedback
from board import Board
class GameEngine:
    '''Core state machine for a single Mastermind game session.'''
    def __init__(self, config, code_generator=None):
        '''
        :param config: GameConfig with palette, code length, max attempts
        :param code_generator: optional CodeGenerator (injectable for tests)
        '''
        self.config = config
        self.code_generator = code_generator or CodeGenerator()
        self.secret = None
        self.board = None
        self.won = False
        self.finished = False
    def start_new_game(self):
        '''Prepare a fresh game: generate the secret and reset the board.'''
        self.secret = self.code_generator.generate(
            self.config.colors.keys(),
            self.config.code_length,
            self.config.allow_duplicates,
        )
        self.board = Board(self.config.code_length, self.config.max_attempts)
        self.won = False
        self.finished = False
    def make_guess(self, guess):
        '''
        Process a validated guess.
        :param guess: list of validated color letters
        :return: Feedback for the guess.
        :raises RuntimeError: if the game is already finished
        '''
        if self.finished:
            raise RuntimeError("The game is already over.")
        feedback = calculate_feedback(self.secret, guess)
        self.board.add_attempt(guess, feedback)
        if feedback.exact_matches == self.config.code_length:
            self.won = True
            self.finished = True
        elif self.board.is_full():
            self.finished = True
        return feedback
    @property
    def attempts_used(self):
        '''Return how many guesses the player has made so far.'''
        return len(self.board.attempts)
    @property
    def attempts_remaining(self):
        '''Return how many guesses the player still has available.'''
        return self.config.max_attempts - self.attempts_used
    def is_over(self):
        '''Return True once the game has been won or lost.'''
        return self.finished