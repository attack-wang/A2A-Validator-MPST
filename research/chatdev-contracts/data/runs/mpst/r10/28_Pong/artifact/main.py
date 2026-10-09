'''
Entry point for the two-player Pong game.
Creates a Game instance and starts the main loop.
Fix for test report ("ModuleNotFoundError: No module named 'pygame'"):
the game modules are imported only after the pygame dependency has been
verified. If pygame is missing it is installed automatically with pip;
if that fails, a clear manual instruction is shown instead of a traceback.
'''
import subprocess
import sys
def ensure_pygame():
    '''Guarantee that pygame is importable, installing it via pip if needed.'''
    try:
        import pygame  # noqa: F401 -- presence check only
        return
    except ImportError:
        pass
    print("pygame is not installed. Attempting automatic installation...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pygame"]
        )
    except subprocess.CalledProcessError:
        print("Automatic installation failed.")
        print("Please install pygame manually with:  pip install pygame")
        sys.exit(1)
def main():
    '''Create and run the Pong game.'''
    ensure_pygame()
    try:
        # Imported here (not at module top level) so the dependency check
        # above always runs before game.py executes "import pygame".
        from game import Game
    except ImportError as exc:
        print(f"Could not load the game: {exc}")
        print("Please install pygame manually with:  pip install pygame")
        sys.exit(1)
    game = Game()
    game.run()
if __name__ == "__main__":
    main()