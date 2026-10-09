'''
main.py
Entry point: launches the graphical interface when tkinter and a display
are available, and falls back to an interactive console mode otherwise.
'''
def main():
    """Launch the GUI; fall back to console mode if no display is available."""
    try:
        import tkinter as tk
    except ImportError:
        tk = None
    if tk is not None:
        try:
            from gui import launch
            launch()
            return
        except tk.TclError:
            print("No display available — falling back to console mode.\n")
    else:
        print("tkinter not available — falling back to console mode.\n")
    from console_ui import run_console_game
    run_console_game()
if __name__ == "__main__":
    main()