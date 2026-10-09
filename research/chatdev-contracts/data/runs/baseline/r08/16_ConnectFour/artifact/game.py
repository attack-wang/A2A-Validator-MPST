'''
game.py
Defines the Game class, which orchestrates a full Connect Four match:
it manages turn order, collects validated moves from the players, applies
them to the board, refreshes the display after every move, and ends the
game when a winning line is detected or the grid is full (draw).
'''
from board import Board
from player import Player
class Game:
    """Controls the flow of a two-player Connect Four game."""
    def __init__(self) -> None:
        """Set up the board and the two players (X moves first)."""
        self.board: Board = Board()
        self.players = [
            Player("Player 1", 'X'),
            Player("Player 2", 'O'),
        ]
        self.current_index: int = 0
    @property
    def current_player(self) -> Player:
        """Return the player whose turn it is right now."""
        return self.players[self.current_index]
    def _switch_turn(self) -> None:
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def play(self) -> None:
        """Run the main game loop until a win, a draw, or a quit."""
        print("=" * 40)
        print("        Welcome to Connect Four!")
        print("=" * 40)
        print("Two players alternate dropping discs into a")
        print("7-column, 6-row grid. The first to line up")
        print("four discs horizontally, vertically, or")
        print("diagonally wins. Type 'q' to quit at any time.")
        self.board.display()
        while True:
            player = self.current_player
            # Ask the current player for a validated column choice.
            col = player.get_move(self.board)
            if col is None:
                print(f"\n{player.name} quit the game. Goodbye!")
                return
            # Apply the move (guaranteed valid by the player's input check).
            row = self.board.drop_disc(col, player.disc)
            self.board.display()
            # A winning line ends the game immediately.
            if self.board.check_win(row, col, player.disc):
                self._announce_win(player)
                return
            # A full grid with no winner is a draw.
            if self.board.is_full():
                self._announce_draw()
                return
            self._switch_turn()
    def _announce_win(self, player: Player) -> None:
        """Print the victory message for the winning player."""
        print("*" * 40)
        print(f"  {player.name} ({player.disc}) connects four and WINS!")
        print("*" * 40)
    def _announce_draw(self) -> None:
        """Print the draw message when the grid is full with no winner."""
        print("=" * 40)
        print("  The grid is full. It's a draw!")
        print("=" * 40)