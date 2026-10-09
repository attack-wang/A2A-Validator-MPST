'''
game.py
Game logic and turn management for the Reversi (Othello) game.
The Game class owns the board, the two players and the console UI,
and drives the full game loop: showing the board and score, reading
moves, flipping discs, passing turns when needed and announcing the
final result.
'''
from board import Board, BLACK, WHITE
from player import Player
from ui import ConsoleUI
class Game:
    '''Manages the flow of a Reversi game between two players.'''
    def __init__(self, player1_name='Player 1', player2_name='Player 2'):
        '''Set up the board, the two players and the console UI.'''
        self.board = Board()
        self.ui = ConsoleUI()
        self.players = [Player(player1_name, BLACK), Player(player2_name, WHITE)]
        self.current_index = 0
    @property
    def current_player(self):
        '''Return the player whose turn it is.'''
        return self.players[self.current_index]
    def switch_turn(self):
        '''Hand the turn over to the other player.'''
        self.current_index = 1 - self.current_index
    def is_game_over(self):
        '''
        Return True when the game has finished: the board is full or
        neither player has any valid move left.
        '''
        if self.board.is_full():
            return True
        return not (self.board.has_any_valid_move(BLACK)
                    or self.board.has_any_valid_move(WHITE))
    def run(self):
        '''Run the main game loop until the game ends or a player quits.'''
        self.ui.display_message('Welcome to Reversi (Othello)!')
        self.ui.display_message('Black moves first. Enter moves as "row col" (1-8), e.g. "3 4".')
        while True:
            player = self.current_player
            valid_moves = self.board.get_valid_moves(player.disc)
            if not valid_moves:
                opponent = self.players[1 - self.current_index]
                if not self.board.has_any_valid_move(opponent.disc):
                    break  # neither player can move -> game over
                self.ui.display_message(
                    f'{player.name} has no valid moves. Turn passes to {opponent.name}.')
                self.switch_turn()
                continue
            self.ui.display_board(self.board, valid_moves)
            self.ui.display_score(self.board, self.players)
            move = self.ui.get_move(player, valid_moves)
            if move is None:
                self.ui.display_message('Game ended by player. Final result:')
                break
            row, col = move
            flipped = self.board.place_disc(row, col, player.disc)
            self.ui.display_message(
                f'{player.name} played ({row + 1}, {col + 1}) and flipped {flipped} disc(s).')
            self.switch_turn()
        self.show_final_result()
    def show_final_result(self):
        '''Display the final board, the final score and the game outcome.'''
        self.ui.display_board(self.board)
        black_score = self.board.count_discs(BLACK)
        white_score = self.board.count_discs(WHITE)
        self.ui.display_message(f'Final score -> Black: {black_score}, White: {white_score}')
        if black_score > white_score:
            self.ui.display_message('Black wins!')
        elif white_score > black_score:
            self.ui.display_message('White wins!')
        else:
            self.ui.display_message("It's a draw!")