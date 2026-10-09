'''
main.py
Entry point of the simplified Space Invaders game. Creates the game
object and starts its main loop. Requires pygame: pip install pygame
'''
from game import SpaceInvadersGame
def main():
    game = SpaceInvadersGame()
    game.run()
if __name__ == "__main__":
    main()