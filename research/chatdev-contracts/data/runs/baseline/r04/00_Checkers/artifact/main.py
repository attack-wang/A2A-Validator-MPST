'''
main.py
Command-line entry point for the checkers game.
Creates the board and players, then runs the interactive loop:
render the board, prompt the current player for a move in coordinate
notation (e.g. "b6-c5" or "b6-d4-f2"), validate it, apply it, and
alternate turns until one side has no legal move. "help" prints the
move syntax, "board" re-renders the board, "quit" exits early.
'''
from board import Board
from game import Game, IllegalMoveError
from move import Move
from piece import PieceColor
from player import Player
HELP_TEXT = """..."""
def main():
    board = Board()
    game = Game(board)
    players = {
        PieceColor.RED: Player("Player 1", PieceColor.RED),
        PieceColor.BLACK: Player("Player 2", PieceColor.BLACK),
    }
    print banner...
    while True:
        print(board.render())
        current = players[game.turn]
        counts...
        if game.is_over():
            winner = players[game.winner()]
            print(f"Game over! {winner.name} ({winner.color.value}) wins!")
            break
        prompt = f"{current.name} ({current.color.value}) - enter move (e.g. b6-c5): "
        text = input(prompt).strip()
        if not text:
            continue
        command = text.lower()
        if command in ("quit", "exit", "q"):
            print("Thanks for playing! Goodbye.")
            break
        if command in ("help", "h", "?"):
            print(HELP_TEXT)
            continue
        if command in ("board", "b"):
            continue  # loop re-renders anyway
        move = Move.parse(text)
        if move is None:
            print("Could not read that move. Use notation like b6-c5 or b6-d4-f2 (type 'help').")
            continue
        try:
            game.apply_move(move)
        except IllegalMoveError as exc:
            print(f"Illegal move: {exc}")
            continue
        # success: loop continues, turn has switched