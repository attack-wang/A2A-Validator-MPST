'''
main.py
Entry point for the Connect Four console application.
Wires together the Board, Player, Game and ui modules, collects
player names, and starts the match loop.
'''
from board import Board
from player import Player
from game import Game
import ui
def main():
    """Set up the board and players, then run one full game."""
    ui.print_welcome()
    board = Board()
    p1_name = ui.get_player_name("Player 1", "X")
    p2_name = ui.get_player_name("Player 2", "O")
    players = (Player(p1_name, "X"), Player(p2_name, "O"))
    game = Game(board, players[0], players[1])
    game.play()
    ui.print_message("Thanks for playing Connect Four!")
if __name__ == "__main__":
    main()