'''
main.py
Entry point for the Gomoku application. Launches the graphical version
by default, or the console version when invoked with '--console'.
'''
import sys
def main():
    """Parse command-line arguments and launch the appropriate interface."""
    if "--console" in sys.argv:
        from console import GomokuConsole
        GomokuConsole().run()
    else:
        import tkinter as tk
        from gui import GomokuGUI
        root = tk.Tk()
        GomokuGUI(root)
        root.mainloop()
if __name__ == "__main__":
    main()