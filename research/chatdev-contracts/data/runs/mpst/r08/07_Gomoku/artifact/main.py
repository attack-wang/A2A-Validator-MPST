'''
main.py
Entry point of the Gomoku application. It wires together the game
components (board, players, renderer) by instantiating GomokuGame
and launching the interactive match loop.
Run with: python main.py
'''
from game import GomokuGame
def main():
    '''Create and run a new Gomoku game session.'''
    game = GomokuGame(board_size=15)
    game.play()
if __name__ == '__main__':
    main()