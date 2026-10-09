'''
Entry point for the Gold Miner game.
'''
import sys
try:
    from game import GoldMinerGame
except ModuleNotFoundError as exc:
    if exc.name == 'pygame':
        print('Error: the "pygame" module is required to run Gold Miner.')
        print('Install it with:  pip install pygame')
        sys.exit(1)
    raise
def main():
    game = GoldMinerGame()
    game.run()
if __name__ == '__main__':
    main()