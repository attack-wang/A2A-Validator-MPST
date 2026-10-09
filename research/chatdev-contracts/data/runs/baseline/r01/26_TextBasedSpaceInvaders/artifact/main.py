'''
main.py
Entry point for the Space Invaders game.
'''
from alien_invasion import AlienInvasion
def main():
    game = AlienInvasion()
    game.run_game()
if __name__ == "__main__":
    main()