'''
game.py
Defines the GomokuGame class, which orchestrates a full Gomoku match:
turn alternation between the two players, applying moves to the board,
detecting wins and draws, and offering rematches after a game ends.
All console prompts are guarded against EOF and KeyboardInterrupt so the
program always terminates gracefully instead of crashing with a traceback.
'''
from board import Board, BLACK, WHITE
from player import Player
from renderer import Renderer
class GomokuGame:
    '''Coordinates the flow of a Gomoku match between two players.'''
    def __init__(self, board_size=15):
        '''Set up the board, the two players, and the console renderer.'''
        self.board_size = board_size
        self.board = Board(board_size)
        self.renderer = Renderer()
        self.players = [
            Player('Player 1 (Black)', BLACK),
            Player('Player 2 (White)', WHITE),
        ]
        self.current_index = 0
    @property
    def current_player(self):
        '''Return the player whose turn it is.'''
        return self.players[self.current_index]
    def switch_player(self):
        '''Hand the turn over to the other player.'''
        self.current_index = 1 - self.current_index
    def reset(self):
        '''Clear the board so a rematch can start from scratch.'''
        self.board = Board(self.board_size)
        self.current_index = 0
    def handle_move(self, player):
        '''Ask the player for a move, apply it, and redraw the board.
        Returns the (row, col) played, or None if the player chose to quit.
        If placement fails, the same player is re-prompted so turn order
        and board state can never fall out of sync.
        '''
        while True:
            move = player.get_move(self.board)
            if move is None:
                return None
            row, col = move
            if self.board.place_stone(row, col, player.stone):
                self.renderer.render_board(self.board)
                return row, col
            self.renderer.show_message(
                'Move could not be placed. Please try again.'
            )
    def check_end(self, row, col, player):
        '''Check whether the last move ended the game.
        Returns 'win', 'draw', or None if the game should continue.
        '''
        if self.board.check_win(row, col):
            self.renderer.show_message(
                f'{player.name} wins with five in a row! Congratulations!'
            )
            return 'win'
        if self.board.is_full():
            self.renderer.show_message('The board is full. It is a draw!')
            return 'draw'
        return None
    def play(self):
        '''Run the main game loop until someone wins, draws, or quits.
        The outer loop handles rematches iteratively (not via recursion),
        so any number of consecutive games can be played without ever
        exhausting Python's call stack.
        '''
        self.renderer.show_message('Welcome to Gomoku (15x15)!')
        self.renderer.show_message('Black plays X, White plays O. Five in a row wins.')
        self.renderer.show_message("Enter moves as 'row col' (0-14), or 'q' to quit.")
        while True:
            self.renderer.render_board(self.board)
            # Inner loop: one complete game (win, draw, or quit).
            while True:
                player = self.current_player
                move = self.handle_move(player)
                if move is None:
                    self.renderer.show_message('Game ended by player. Goodbye!')
                    return
                row, col = move
                result = self.check_end(row, col, player)
                if result in ('win', 'draw'):
                    break
                self.switch_player()
            # Outer loop: rematch handling without recursion.
            if not self.offer_rematch():
                self.renderer.show_message('Thanks for playing Gomoku. Goodbye!')
                return
            self.reset()
    def offer_rematch(self):
        '''Ask whether the players want another round.
        Returns True when the players choose to rematch, False otherwise.
        EOFError and KeyboardInterrupt are caught and treated as a "no",
        so an exhausted stdin or user interrupt exits cleanly through the
        normal goodbye path instead of raising an unhandled exception.
        '''
        try:
            answer = input('Play again? (y/n): ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()  # keep output tidy after the interrupted prompt
            return False
        return answer in ('y', 'yes')