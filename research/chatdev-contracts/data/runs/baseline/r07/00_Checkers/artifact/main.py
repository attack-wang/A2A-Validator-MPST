'''
main.py - Entry point: interactive console loop for the Checkers game.
'''
from pieces import RED, BLACK
from game import Game
from move import Move, square_name, parse_square
def parse_move_input(text, game):
    """Parse 'from-to' notation into a Move, validated against legal moves."""
    text = text.strip().lower().replace("x", "-")
    parts = text.split("-")
    if len(parts) != 2:
        raise ValueError("Move must be in 'from-to' format, e.g., 'b6-a5'.")
    from_pos = parse_square(parts[0])
    to_pos = parse_square(parts[1])
    for move in game.legal_moves():
        if move.from_pos == from_pos and move.to_pos == to_pos:
            return move
    raise ValueError("That move is not legal. Type 'help' to see hints.")
def main():
    game = Game()
    print(banner)
    while not game.game_over:
        print(game.board.render())
        ... prompt