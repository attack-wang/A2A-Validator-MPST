'''
main.py
Entry point for the simplified Space Invaders game. Creates the Game
instance and starts the main loop; exits cleanly when the window closes.
'''
from game import Game
if __name__ == "__main__":
    Game().run()