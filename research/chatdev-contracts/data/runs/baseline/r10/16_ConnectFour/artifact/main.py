'''
main.py
Entry point of the Connect Four application. Builds a Game instance
and starts the interactive session.
'''
from game import Game
def main() -> None:
    '''Create the game and run it until the players quit.'''
    game = Game()
    game.run()
if __name__ == '__main__':
    main()