class GameUI:
    """Tkinter view + controller for the 2048 game."""
    CELL_SIZE = 90
    CELL_GAP = 10
    BOARD_PADDING = 10
    CORNER_RADIUS = 6
    BG_COLOR = '#faf8ef'
    BOARD_COLOR = '#bbada0'
    EMPTY_COLOR = '#cdc1b4'
    TEXT_COLOR = '#776e65'
    LIGHT_TEXT_COLOR = '#f9f6f2'
    SCORE_BOX_BG = '#bbada0'
    SCORE_LABEL_COLOR = '#eee4da'
    SCORE_VALUE_COLOR = '#ffffff'
    OVERLAY_COLOR = '#faf8ef'
    def __init__(self, master=None):
        self.root = tk.Tk() if master is None else master
        self.root.title('2048')
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self.game = Game2048()
        self._build_header()
        self._build_board()
        self._bind_keys()
        self.redraw()