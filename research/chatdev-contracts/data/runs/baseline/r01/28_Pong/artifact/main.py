'''
main.py
Entry point of the two-player Pong game. It first verifies that the
required pygame dependency is available (attempting an automatic pip
installation when it is missing), then creates the Game instance and
starts the main loop.
'''
import subprocess
import sys
def ensure_pygame_installed():
    '''Ensure pygame is importable; install it via pip automatically if missing.'''
    try:
        import pygame  # noqa: F401
        return
    except ModuleNotFoundError:
        print("pygame is not installed. Attempting automatic installation...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("pygame installed successfully.")
    except (subprocess.CalledProcessError, OSError):
        print("Automatic installation failed.")
        print("Please install it manually with: pip install pygame")
        sys.exit(1)
def main():
    '''Create and run the Pong game.'''
    ensure_pygame_installed()
    from game import Game
    game = Game()
    game.run()
if __name__ == "__main__":
    main()