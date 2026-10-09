class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku — ChatDev Edition")
        self.root.resizable(False, False)
        self.generator = PuzzleGenerator()
        self.board = None
        self.solution = None
        self.selected = None  # (row, col) or None
        self.elapsed = 0
        self.timer_job = None
        self.game_over = False
        self._build_menu()
        self._build_widgets()
        self.new_game("easy")
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game — Easy", command=lambda: self.new_game("easy"))
        game_menu.add_command(label="New Game — Medium", command=lambda: self.new_game("medium"))
        game_menu.add_command(label="New Game — Hard", command=lambda: self.new_game("hard"))
        game_menu.add_separator()
        game_menu.add_command(label="Restart Puzzle", command=self.restart)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
    def _build_widgets(self):
        top = tk.Frame(self.root, bg=BG_COLOR)
        ...