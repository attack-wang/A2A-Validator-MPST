'''
main.py
Entry point for the Gomoku application. Launches the graphical
interface when Tkinter is available and falls back to the
console interface otherwise.
'''
from game import Game
def gui_available():
    '''Return True only if a Tkinter window can actually be created.'''
    try:
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:  # covers ImportError and tk.TclError (headless systems)
        return False
def main():
    '''Launch the Gomoku game, preferring the GUI and falling back to console.'''
    game = Game()
    ui = None
    if gui_available():
        try:
            from gui import GomokuGUI
            ui = GomokuGUI(game)
        except Exception as exc:
            print(f'Graphical interface unavailable ({exc}); falling back to console mode.')
            ui = None
    if ui is None:
        from console_ui import ConsoleUI
        ConsoleUI(game).run()
    else:
        ui.run()
if __name__ == '__main__':
    main()