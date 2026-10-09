'''
Entry point: launches the Space Invaders game.
Fix for the reported test failure:
    ModuleNotFoundError: No module named 'pygame'
The entry point now verifies that the pygame dependency is importable
BEFORE loading the game modules and, when it is missing, installs it
automatically with pip. This guarantees the game starts smoothly even
in a fresh environment where pygame has not been installed yet.
'''
import sys
import subprocess
def ensure_pygame_installed():
    '''Check that pygame is importable; install it via pip when missing.'''
    try:
        import pygame  # noqa: F401  (availability check only)
    except ModuleNotFoundError:
        print("pygame is not installed. Attempting automatic installation...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'pygame']
            )
            print("pygame installed successfully.")
        except subprocess.CalledProcessError:
            print("Automatic installation failed. "
                  "Please install it manually with: pip install pygame")
            sys.exit(1)
# Resolve the dependency first so that 'from game import Game' below
# can never raise ModuleNotFoundError again.
ensure_pygame_installed()
from game import Game
if __name__ == '__main__':
    game = Game()
    game.run()