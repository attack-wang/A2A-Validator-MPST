'''
main.py
Entry point of the Gomoku (Five in a Row) application.
It creates the Game object and launches the graphical user interface
when tkinter is available; otherwise it falls back to a text-based
console interface so the game can run anywhere.
Run with:  python main.py
'''
import sys
from game import Game
def main():
    """Create a new Gomoku game and start the appropriate user interface."""
    game = Game(player1_name="Black", player2_name="White")
    try:
        import tkinter  # noqa: F401  (availability check)
        from gui import GomokuGUI
        GomokuGUI(game).run()
        return
    except ImportError:
        pass  # tkinter not installed -> fall back to console
    except Exception as exc:
        # e.g. tkinter present but no display server (headless environment)
        print(f"Graphical interface unavailable ({exc}); switching to console mode.")
    from console import ConsoleUI
    ConsoleUI(game).run()
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame aborted. Goodbye!")
        sys.exit(0)