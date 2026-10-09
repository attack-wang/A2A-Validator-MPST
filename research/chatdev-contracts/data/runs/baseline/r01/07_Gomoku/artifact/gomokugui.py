class GomokuGUI:
    """Tkinter window that renders the board and handles player interaction."""
    def __init__(self, master, controller):
        self._master = master
        self._controller = controller
        master.title("Gomoku - Five in a Row")
        master.resizable(False, False)
        self._canvas = tk.Canvas(master, width=WINDOW_WIDTH,
                                 height=WINDOW_HEIGHT,
                                 bg=BOARD_COLOR, highlightthickness=0)
        self._canvas.pack()
        self._status_label = tk.Label(master, text="", font=("Helvetica", 14, "bold"),
                                      fg=TEXT_COLOR, bg=...)