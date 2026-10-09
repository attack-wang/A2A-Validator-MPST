'''
main.py
Entry point of the Reversi (Othello) console game. It creates the two
players, builds the Game object and starts the match.
'''
from board import BLACK, WHITE
from game import Game
from player import Player
def prompt_player_name(default_name):
    '''Ask for a player name, falling back to the default when empty.'''
    try:
        entered = input(f'Name for {default_name} (Enter to keep default): ').strip()
    except EOFError:
        entered = ''
    return entered or default_name
def main():
    '''Set up the players, start the game and handle a graceful exit.'''
    print('Welcome to Reversi (Othello)!')
    try:
        black_player = Player(BLACK, prompt_player_name('Player 1 (X)'))
        white_player = Player(WHITE, prompt_player_name('Player 2 (O)'))
        game = Game(black_player, white_player)
        game.run()
    except (KeyboardInterrupt, EOFError):
        print('\nGame interrupted. Thanks for playing - goodbye!')
        return 0
    return 0
if __name__ == '__main__':
    main()