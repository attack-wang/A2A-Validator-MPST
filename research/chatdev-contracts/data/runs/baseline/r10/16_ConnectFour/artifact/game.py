'''
game.py
Defines the Game class, which orchestrates a Connect Four session:
player setup, alternating turns, move validation, and win/draw handling.
'''
from board import Board
from player import Player
from config import DISC_ONE, DISC_TWO, DEFAULT_NAME_ONE, DEFAULT_NAME_TWO
class Game:
    '''Runs a full Connect Four match between two human players.'''
    def __init__(self) -> None:
        '''Prepare an empty board and an empty player list.'''
        self.board = Board()
        self.players = []
        self.current_index = 0
    @property
    def current_player(self) -> Player:
        '''Return the player whose turn it is.'''
        return self.players[self.current_index]
    def switch_player(self) -> None:
        '''Hand the turn over to the other player.'''
        self.current_index = 1 - self.current_index
    def ask_name(self, number: int, default: str) -> str:
        '''Prompt for a player's name, falling back to the default if blank.'''
        raw = input(f'Enter name for Player {number} (default: {default}): ').strip()
        return raw or default
    def setup_players(self) -> None:
        '''Greet the users and create the two players.'''
        print('Welcome to Connect Four!')
        print(f'Two players alternate dropping discs into a '
              f'{self.board.columns}-column, {self.board.rows}-row grid.')
        print(f'The first to line up {self.board.connect} discs horizontally, '
              f'vertically, or diagonally wins.\n')
        name_one = self.ask_name(1, DEFAULT_NAME_ONE)
        name_two = self.ask_name(2, DEFAULT_NAME_TWO)
        self.players = [Player(name_one, DISC_ONE), Player(name_two, DISC_TWO)]
        print(f'\n{self.players[0].name} plays "{DISC_ONE}", '
              f'{self.players[1].name} plays "{DISC_TWO}". {name_one} goes first.')
    def play_round(self) -> str:
        '''Play one game to completion; return "win" or "draw".'''
        self.board = Board()
        self.current_index = 0
        while True:
            print()
            print(self.board.render())
            column = self.current_player.choose_column(self.board)
            row = self.board.drop_disc(column, self.current_player.disc)
            winning_line = self.board.check_win_from(row, column, self.current_player.disc)
            if winning_line is not None:
                print()
                print(self.board.render(highlight=winning_line))
                self.announce_winner()
                return 'win'
            if self.board.is_full():
                print()
                print(self.board.render())
                self.announce_draw()
                return 'draw'
            self.switch_player()
    def announce_winner(self) -> None:
        '''Print the victory message for the current player.'''
        winner = self.current_player
        print(f'\n*** {winner.name} ({winner.disc}) connects {self.board.connect} '
              f'and wins the game! ***')
    def announce_draw(self) -> None:
        '''Print the draw message.'''
        print('\n*** The grid is full. It\'s a draw! ***')
    def ask_replay(self) -> bool:
        '''Ask whether to play again; return True for yes.'''
        while True:
            answer = input('\nPlay again? (y/n): ').strip().lower()
            if answer in ('y', 'yes'):
                return True
            if answer in ('n', 'no'):
                return False
            print("Please answer 'y' or 'n'.")
    def run(self) -> None:
        '''Set up the players and keep playing rounds until the users quit.'''
        try:
            self.setup_players()
            while True:
                self.play_round()
                if not self.ask_replay():
                    print('\nThanks for playing Connect Four. Goodbye!')
                    break
        except (KeyboardInterrupt, EOFError):
            print('\nGame interrupted. Goodbye!')