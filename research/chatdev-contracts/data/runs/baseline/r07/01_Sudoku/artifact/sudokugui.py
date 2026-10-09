class SudokuGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.selected = (0, 0)
        self.game_over = False
        self.start_time = time.time()
        self.timer_running = True
        self.auto_check_var = tk.BooleanVar(value=True)
        self.difficulty_var = tk.StringVar(value="Medium")
        self.root.title("Sudoku — ChatDev Edition")
        self.root.resizable(False, False)
        self._build_widgets()
        self._bind_events()
        self.redraw()
        self._tick_timer()