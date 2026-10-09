'''
main.py
Entry point for the two-player Pong game.
Fixes the reported ModuleNotFoundError by guaranteeing that the 'pygame'
dependency is available before the game modules are imported: if pygame
is missing, it is installed automatically via pip; if that fails, a clear
manual-installation hint is shown and the program exits gracefully.
'''
import subprocess
import sys
def ensure_pygame():
    '''Import pygame, installing it automatically via pip when missing.'''
    try:
        import pygame  # noqa: F401  (dependency check only)
        return
    except ModuleNotFoundError:
        print("[setup] 'pygame' not found. Attempting automatic installation ...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pygame"]
            )
        except (subprocess.CalledProcessError, OSError) as exc:
            print("[setup] Automatic installation failed: %s" % exc)
            print("[setup] Please install pygame manually with: pip install pygame")
            sys.exit(1)
        try:
            import pygame  # noqa: F401  (verify installation succeeded)
        except ModuleNotFoundError:
            print("[setup] pygame is still unavailable after installation.")
            sys.exit(1)
def main():
    '''Create and run the Pong game after verifying dependencies.'''
    ensure_pygame()
    # Imported here (not at module top) so pygame is guaranteed present.
    from game import Game
    game = Game()
    game.run()
if __name__ == "__main__":
    main()