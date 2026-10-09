def main():
    """Launch the Mastermind game (GUI if possible, console otherwise)."""
    try:
        import tkinter as tk
        from mastermindgui import MastermindGUI
    except ImportError:
        print('tkinter is not available - switching to console mode.\n')
        from console_ui import play_console_game
        play_console_game()
        return
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        print('Cannot open a graphical window ({}).'.format(exc))
        print('Switching to console mode.\n')
        from console_ui import play_console_game
        play_console_game()
        return
    MastermindGUI(root)
    root.mainloop()
if __name__ == '__main__':
    main()