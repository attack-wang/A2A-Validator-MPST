'''
main.py
Entry point for the Mastermind code-breaking game.
Creates Game sessions and offers replays until the player chooses
to exit.
'''
from game import Game
def ask_replay():
    '''Ask the player whether to start another game. Returns True for yes.'''
    while True:
        answer = input('Play again? (y/n): ').strip().lower()
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        print('  Please answer "y" or "n".')
def main():
    '''Run Mastermind sessions in a loop until the player quits.'''
    print('Welcome to Mastermind!')
    while True:
        game = Game()
        game.play()
        if not ask_replay():
            break
    print('Thanks for playing Mastermind. Goodbye!')
if __name__ == '__main__':
    main()