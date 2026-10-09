'''
Entry point for the interactive storytelling game.
Boots the GameEngine, which presents the title banner, handles the
main menu (new game / load game / quit), and runs the branching
narrative loop until the player reaches an ending.
'''
from engine import GameEngine
if __name__ == "__main__":
    GameEngine().run()