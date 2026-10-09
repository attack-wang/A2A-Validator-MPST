'''
main.py
Entry point for the Gomoku application. Launches either the graphical
(tkinter) interface by default, or the console interface when run with
the "--console" flag. If the GUI cannot be loaded for any reason
(missing tkinter, or any error raised while importing the GUI module),
the application falls back to the console interface so the game always
remains playable.
'''
import sys
from game import GomokuGame
def main():
    if "--console" in sys.argv:
        from console_ui import ConsoleUI
        game = GomokuGame()
        ui = ConsoleUI(game)
        ui.run()
    else:
        try:
            import tkinter as tk
            from gui import GomokuGUI
        except Exception:
            # Catch ImportError (tkinter missing) as well as any error
            # raised inside gui.py during import, so a broken GUI module
            # can never crash the whole application.
            print("GUI unavailable; falling back to console mode.")
            from console_ui import ConsoleUI
            game = GomokuGame()
            ui = ConsoleUI(game)
            ui.run()
            return
        root = tk.Tk()
        GomokuGUI(root)
        root.mainloop()
if __name__ == "__main__":
    main()