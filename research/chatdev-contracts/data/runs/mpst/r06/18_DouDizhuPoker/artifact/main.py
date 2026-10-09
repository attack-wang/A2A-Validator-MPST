'''Main entry point: starts a console Dou Dizhu game with one human and two AI players.'''
from game import Game
def main():
    print banner
    game = Game(['You', 'AI-1', 'AI-2'])
    game.run()
if __name__ == '__main__':
    main()