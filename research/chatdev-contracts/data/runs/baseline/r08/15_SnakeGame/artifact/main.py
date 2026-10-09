'''
main.py
Entry point: verifies the pygame dependency and launches the Snake game.
'''
import sys
try:
    import pygame
except ImportError:
    sys.exit("pygame is required. Install it with: pip install pygame")
from game import Game
def main():
    Game().run()
if __name__ == "__main__":
    main()