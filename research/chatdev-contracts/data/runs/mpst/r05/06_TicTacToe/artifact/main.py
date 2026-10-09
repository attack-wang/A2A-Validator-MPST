'''
main.py
Entry point of the Tic-Tac-Toe application. Launches the graphical
user interface by default; pass --console on the command line to play
in the terminal instead (useful on systems without a display or when
Tkinter is unavailable).
'''
import sys
def main():
    """Start the tic-tac-toe application in the requested mode."""
    console_mode = "--console" in sys.argv[1:]
    if console_mode:
        from console_ui import ConsoleUI
        from game_logic import TicTacToeGame
        ConsoleUI(TicTacToeGame()).run()
        return
    try:
        import tkinter as tk
    except ImportError:
        print("Tkinter is not available; falling back to console mode.\n")
        from console_ui import ConsoleUI
        from game_logic import TicTacToeGame
        ConsoleUI(TicTacToeGame()).run()
        return
    from game_logic import TicTacToeGame
    from gui import TicTacToeGUI
    try:
        root = tk.Tk()
    except tk.TclError:
        # No graphical display (e.g. headless server) -> console fallback.
        print("No graphical display available; falling back to console mode.\n")
        from console_ui import ConsoleUI
        ConsoleUI(TicTacToeGame()).run()
        return
    TicTacToeGUI(root, TicTacToeGame())
    root.mainloop()
if __name__ == "__main__":
    main()