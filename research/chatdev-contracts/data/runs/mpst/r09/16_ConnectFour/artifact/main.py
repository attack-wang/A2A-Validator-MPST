'''
main.py
Entry point for the Connect Four game. Creates the board and the two
players, wires them into the Game, and starts the interactive loop.
'''
from board import Board
from game import Game
from player import Player
def main():
    """Set up a standard Connect Four match and run it to completion."""
    board = Board(rows=Board.ROWS, cols=Board.COLS)
    players = [
        Player("Player 1", "X"),
        Player("Player 2", "O"),
    ]
    game = Game(board, players)
    game.play()
if __name__ == "__main__":
    main()