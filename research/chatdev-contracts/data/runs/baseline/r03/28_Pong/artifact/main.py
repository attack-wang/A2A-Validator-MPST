'''
main.py
Entry point of the two-player Pong game.
Run this file to start the game:
    python main.py
Controls:
    Player 1 (left paddle):  W (up) / S (down)
    Player 2 (right paddle): Up arrow / Down arrow
    SPACE starts the match / a rematch, ESC quits.
'''
from game import Game
if __name__ == '__main__':
    Game().run()