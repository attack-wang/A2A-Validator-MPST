class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        self.board = SudokuBoard()
        self.generator = SudokuGenerator()
        self.selected = None  # (row, col) or None
        self.mistakes = 0
        self.elapsed = 0
        self.timer_running = False
        self.game_over = False
        self._build_menu_bar()
        self._build_top_bar()
        self._build_canvas()
        self._build_bottom_bar()
        self.root.bind("<Key>", self.on_key)
        self.new_game("Easy")
    def _build_menu_bar(self):
        ...
    def _build_top_bar(self):
        # New Game button, difficulty combobox, timer, mistakes
        ...
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, width=BOARD_PX, height=BOARD_PX, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(padx=10, pady=5)
        self.canvas.bind("<Button-1>", self.on_click)
        self._draw_grid_lines()
    def _build_bottom_bar(self):
        # Check, Hint, Erase buttons + status label
        ...