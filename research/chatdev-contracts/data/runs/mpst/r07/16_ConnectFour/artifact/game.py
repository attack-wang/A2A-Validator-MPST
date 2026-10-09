'''
game.py
Defines the Game class that orchestrates a full Connect Four match.
The Game owns the Board and the two Players, alternates turns, applies
each move to the board, checks for a win or a draw after every move, and
announces the final result. If the input stream is exhausted or the
session is interrupted mid-match, the game ends gracefully with an
informative message instead of an unhandled traceback.
'''
from board import Board
from player import Player
DEFAULT_PLAYERS = (
    Player('Player 1', 'X'),
    Player('Player 2', 'O'),
)
class Game:
    '''Coordinates turn-taking and end-of-game detection for Connect Four.'''
    def __init__(self, board=None, players=None):
        '''Set up the board and players (defaults: 6x7 board, X vs O).'''
        self.board = board if board is not None else Board()
        self.players = list(players) if players is not None else list(DEFAULT_PLAYERS)
        self.current_index = 0
        self.winner = None
        self.ended_early = False
    @property
    def current_player(self):
        '''Return the player whose turn it is.'''
        return self.players[self.current_index]
    def switch_player(self):
        '''Hand the turn over to the other player.'''
        self.current_index = (self.current_index + 1) % len(self.players)
    def take_turn(self):
        '''
        Run a single turn: prompt the current player, drop their disc,
        render the updated board, and report whether the game has ended.
        Returns True when the game is over (win, draw, or the input
        stream closed / was interrupted).
        '''
        player = self.current_player
        column = player.get_move(self.board)
        if column is None:
            # The player could not supply a move (EOF on stdin or an
            # interrupt): end the match gracefully rather than crashing.
            self.ended_early = True
            return True
        row = self.board.drop_disc(column, player.disc)
        if row is None:
            # Defensive fallback: the column became invalid between the
            # prompt and the drop; let the same player try again.
            print('That column cannot accept a disc right now. Try again.')
            return False
        winning_line = self.board.check_win(row, column - 1, player.disc)
        if winning_line:
            self.winner = player
            self.board.render(highlight=winning_line)
            return True
        if self.board.is_full():
            self.board.render()
            return True
        self.board.render()
        self.switch_player()
        return False
    def announce_result(self):
        '''Print the final outcome of the match.'''
        print()
        if self.ended_early:
            print('The match ended early: no further input was available.')
        elif self.winner is not None:
            print(f'*** {self.winner.name} ({self.winner.disc}) connects four and wins! ***')
        else:
            print("*** The board is full — it's a draw! ***")
    def play(self):
        '''Run the game loop until a player wins, the grid fills up, or input ends.'''
        print('=== Connect Four ===')
        print(f'Players: {self.players[0].name} ({self.players[0].disc}) vs '
              f'{self.players[1].name} ({self.players[1].disc})')
        print('Type a column number (1-7) on your turn to drop a disc.')
        print('First to connect four in a row — horizontally, vertically, '
              'or diagonally — wins.\n')
        self.board.render()
        while not self.take_turn():
            pass
        self.announce_result()