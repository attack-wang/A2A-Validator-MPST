'''
Entry point for the two-player Pong game.
Ensures the pygame dependency is available (auto-installing it via
pip when missing), then creates the Game instance (which owns the
pygame window and main loop) and runs it until the player quits.
'''
import importlib
import subprocess
import sys
def _install_pygame():
    """
    Install pygame with pip; fall back to a per-user installation if
    the global installation is not permitted on this system.
    """
    print("pygame is not installed - installing it automatically ...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pygame"]
        )
    except subprocess.CalledProcessError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user", "pygame"]
        )
def _ensure_pygame():
    """
    Import pygame, installing it automatically when the module is
    missing so the game starts without any manual dependency setup.
    """
    try:
        import pygame  # noqa: F401
    except ModuleNotFoundError:
        _install_pygame()
        importlib.invalidate_caches()
        import pygame  # noqa: F401
def main():
    """Boot the game and run the main loop (pygame is shut down inside Game.run)."""
    _ensure_pygame()
    from game import Game  # imported late: game.py requires pygame to exist
    game = Game()
    game.run()
if __name__ == "__main__":
    main()