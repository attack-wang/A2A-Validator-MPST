'''
main.py
Entry point: sets up the game loop, alternates turns between the two
players, applies moves, and detects game over.
'''
from pieces import RED, BLACK
from board import Board
from player import Player, QuitGame
class CheckersGame:
    def __init__(self):
        self.board = Board()
        self.players = {RED: Player(RED, 'Red'), BLACK: Player(BLACK, 'Black')}
        self.turn = RED
    def legal_moves(self, color):
        return self.board.get_all_moves(color)
    def run(self):
        self._print_intro()
        while True:
            player = self.players[self.turn]
            legal = self.legal_moves(self.turn)
            if not legal:
                opponent = self.players[self._other(self.turn)]
                print(f"\n{player.name} has no pieces or no legal moves — {opponent.name} wins!")
                break
            self.board.display()
            print(f"\n{player.name} to move.")
            path = player.get_move(self)
            result = self.board.apply_move(path)
            move_str = '-'.join(Player.square_name(sq) for sq in path)
            if result.captured:
                print(f"{move_str}: {player.name} captured {len(result.captured)} piece(s)!")
            else:
                print(f"{move_str}: move applied.")
            if result.kinged:
                print(f"{player.name}'s piece reached the back rank and is now a KING!")
            self.turn = self._other(self.turn)
    @staticmethod
    def _other(color):
        return BLACK if color == RED else RED
    @staticmethod
    def _print_intro():
        print(...rules intro...)
def main():
    try:
        CheckersGame().run()
    except QuitGame:
        print("\nGame ended. Goodbye!")
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
if __name__ == '__main__':
    main()