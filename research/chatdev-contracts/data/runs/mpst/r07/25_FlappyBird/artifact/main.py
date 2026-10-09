'''
main.py
Entry point for the Flappy Bird clone. Verifies that the pygame
dependency is importable (auto-installing it via pip when missing)
and then starts the game loop.
'''
import importlib
import subprocess
import sys
def _ensure_package(package):
    """Import `package`, installing it with pip when it is missing."""
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"'{package}' not found - installing it now ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package]
        )
        importlib.invalidate_caches()
        importlib.import_module(package)
_ensure_package("pygame")
from game import Game  # noqa: E402  (import must follow the dependency check)
def main():
    """Create the Game instance and run the main loop."""
    Game().run()
if __name__ == "__main__":
    main()