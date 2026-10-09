'''
main.py
Entry point for the Classic Snake game.
Wires up pygame, shows the difficulty menu, then runs game sessions
until the player quits. If the pygame dependency is missing, a one-time
automatic installation via pip is attempted; if that fails (e.g. no
network), a clear manual installation hint is printed and the program
exits cleanly instead of raising a raw ModuleNotFoundError traceback.
'''
import subprocess
import sys
def _ensure_pygame():
    """Import pygame; if missing, try to install it once, then re-import.
    Returns the pygame module. Exits with a helpful message when the
    dependency cannot be made available automatically.
    """
    try:
        import pygame
        return pygame
    except ImportError:
        pass  # dependency absent -> try automatic installation below
    print("'pygame' is not installed - attempting automatic installation...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pygame>=2.0.0"],
            timeout=180,
        )
    except Exception as exc:
        print("=" * 62)
        print("Automatic installation failed: {}".format(exc))
        print("Please install pygame manually, then run the game again:")
        print("    python -m pip install pygame")
        print("or: python -m pip install -r requirements.txt")
        print("=" * 62)
        sys.exit(1)
    # Fresh import now that the package has been installed.
    import pygame
    return pygame
pygame = _ensure_pygame()
import settings
from menu import Menu
from game import Game
def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Classic Snake")
    while True:
        difficulty = Menu(screen).run()  # difficulty name, or None to quit
        if difficulty is None:
            break
        while True:
            action = Game(screen, difficulty).run()  # "menu"/"quit"/"restart"
            if action == "quit":
                pygame.quit()
                sys.exit()
            if action == "menu":
                break
            # action == "restart": loop again with the same difficulty
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()