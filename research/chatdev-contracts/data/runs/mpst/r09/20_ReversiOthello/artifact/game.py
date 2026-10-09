'''
game.py
Implements the Game class, which orchestrates a full Reversi match:
alternating turns between the two players, applying moves and flipping
discs, displaying the running score, and detecting when the game is
over (board full or no valid moves remaining).
'''
from board import Board, BLACK, WHITE, COLUMNS
class Game:
    '''Coordinates two players taking turns on a shared Reversi board.'''
    def __init__(self, black_player, white_player):
        '''Create the board, bind each player to a disc color and set
        black (who always moves first in Reversi) as the starting player.'''
        self.board = Board()
        self.players = {BLACK: black_player, WHITE: white_player}
        self.current_color = BLACK
    @property
    def current_player(self):
        '''Return the Player whose turn it currently is.'''
        return self.players[self.current_color]
    def switch_turn(self):
        '''Pass the turn to the other player.'''
        self.current_color = WHITE if self.current_color == BLACK else BLACK
    def is_game_over(self):
        '''Return True when the board is full or neither player can move.'''
        if self.board.is_full():
            return True
        return not (self.board.get_valid_moves(BLACK)
                    or self.board.get_valid_moves(WHITE))
    def display_score(self):
        '''Print the current number of discs held by each player.'''
        black, white = self.board.count_discs()
        print(f'Score  ->  {self.players[BLACK].name} (X): {black}   |   '
              f'{self.players[WHITE].name} (O): {white}')
    def announce_result(self):
        '''Show the final board and score, then declare the winner or a tie.'''
        print()
        print('=' * 40)
        print('FINAL RESULT')
        print('=' * 40)
        self.board.display()
        self.display_score()
        black, white = self.board.count_discs()
        if black > white:
            print(f'{self.players[BLACK].name} (X) wins, {black} to {white}!')
        elif white > black:
            print(f'{self.players[WHITE].name} (O) wins, {white} to {black}!')
        else:
            print(f'The game ends in a tie, {black} to {white}!')
    def run(self):
        '''Execute the main game loop until the game is over.'''
        print('=' * 40)
        print('       REVERSI (OTHELLO)')
        print('=' * 40)
        print(f'{self.players[BLACK].name} plays X (black) and moves first.')
        print(f'{self.players[WHITE].name} plays O (white).')
        print('Enter moves as "d3" or as "row col" such as "3 4".')
        print('Legal moves for the current player are marked with "*".')
        while not self.is_game_over():
            player = self.current_player
            valid_moves = self.board.get_valid_moves(player.color)
            if not valid_moves:
                # The other side may still have moves, so this player passes.
                print(f'\n{player.name} ({player.symbol}) has no legal move '
                      'and must pass.')
                self.switch_turn()
                continue
            print()
            print('-' * 40)
            print(f"{player.name}'s turn ({player.symbol}).")
            self.board.display(valid_moves)
            self.display_score()
            row, col = player.choose_move(valid_moves)
            flipped = self.board.place_disc(player.color, row, col)
            print(f'{player.name} played '
                  f'{COLUMNS[col]}{row + 1} and flipped {flipped} disc(s).')
            self.switch_turn()
        self.announce_result()