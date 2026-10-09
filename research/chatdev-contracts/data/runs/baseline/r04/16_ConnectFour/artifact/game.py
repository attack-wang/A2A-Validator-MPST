'''
game.py
Orchestrates a full Connect Four match: builds the two players, runs the
turn loop, validates every column choice, applies moves to the board and
detects wins or draws, announcing the result when the game ends.
'''
from board import Board
from exceptions import ColumnFullError, InvalidColumnError
from player import Player
class Game:
    """Controls the flow of a two-player Connect Four match."""
    def __init__(self, player_one_name='Player 1', player_two_name='Player 2'):
        """Create a fresh board and the two players; Player 1 moves first."""
        self._board = Board()
        self._players = (
            Player(player_one_name, 'X'),
            Player(player_two_name, 'O'),
        )
        self._current_index = 0
    @property
    def current_player(self):
        """Return the Player whose turn it is right now."""
        return self._players[self._current_index]
    def _switch_player(self):
        """Hand the turn over to the other player."""
        self._current_index = 1 - self._current_index
    def _get_valid_move(self, player):
        """
        Keep prompting `player` until they type a legal column number.
        Returns:
            int: A validated 1-based column that still has at least one
            free cell.
        """
        while True:
            try:
                column = player.choose_column(self._board.columns)
                self._board.is_valid_column(column)
                return column
            except (InvalidColumnError, ColumnFullError) as error:
                print(f"  [!] {error}")
    def play(self):
        """Run the match from the first move until a win or a draw."""
        self._print_intro()
        self._board.display()
        while True:
            player = self.current_player
            column = self._get_valid_move(player)
            row, col = self._board.drop_disc(column, player.disc)
            print(f"{player.name} dropped {player.disc} into column {column}.")
            self._board.display()
            if self._board.check_win(row, col, player.disc):
                self._announce_winner(player)
                return
            if self._board.is_full():
                self._announce_draw()
                return
            self._switch_player()
    def _print_intro(self):
        """Print the welcome banner and a short rules summary."""
        print("=" * 46)
        print("                CONNECT FOUR")
        print("=" * 46)
        print(f"{self._players[0]}  vs  {self._players[1]}")
        print("On your turn, type a column number (1-7) to drop a disc.")
        print("Align four discs horizontally, vertically or diagonally")
        print("to win. A full board with no line of four is a draw.")
        print("=" * 46)
    def _announce_winner(self, player):
        """Print the final banner declaring `player` the winner."""
        print("=" * 46)
        print(f"   {player.name} ({player.disc}) WINS - four in a row!")
        print("=" * 46)
    def _announce_draw(self):
        """Print the final banner for a drawn (full-board) game."""
        print("=" * 46)
        print("   The board is full - the game ends in a DRAW!")
        print("=" * 46)