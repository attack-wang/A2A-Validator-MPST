'''
main.py
Entry point for the Gold Miner game. Creates the Game instance and runs
the main loop.
Fix for the reported test failure:
    ModuleNotFoundError: No module named 'pygame'
The entry point now checks that pygame is importable BEFORE importing the
game modules. If pygame is missing, it attempts to install it automatically
via pip and then continues startup; if the installation fails, it prints a
clear manual instruction and exits gracefully instead of raising an
unhandled traceback.
'''
import importlib
import subprocess
import sys
def ensure_pygame():
    '''Guarantee that pygame is importable, installing it via pip if needed.'''
    try:
        importlib.import_module('pygame')
        return
    except ImportError:
        pass
    print("'pygame' was not found. Attempting automatic installation via pip ...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    except subprocess.CalledProcessError as exc:
        print("ERROR: automatic installation of 'pygame' failed "
              "(pip exit code {}).".format(exc.returncode))
        print("Please install it manually with:  pip install pygame")
        sys.exit(1)
    try:
        importlib.import_module('pygame')
        print("'pygame' installed successfully. Starting the game ...")
    except ImportError:
        print("ERROR: 'pygame' still cannot be imported after installation.")
        print("Please install it manually with:  pip install pygame")
        sys.exit(1)
# Make sure pygame exists BEFORE importing game modules that depend on it.
ensure_pygame()
import pygame  # noqa: E402  (availability guaranteed by ensure_pygame above)
from game import Game  # noqa: E402
import settings  # noqa: E402
def main():
    '''Create the Game instance and run the main loop.'''
    game = Game()
    game.run()
if __name__ == '__main__':
    main()