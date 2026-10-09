class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Sudoku')
        self.root.resizable(False, False)
        self.board = SudokuBoard()
        self.selected = None  # (row, col) or None
        self.mistake_cells = set()
        self.completed = False
        self.elapsed = 0
        self.timer_running = False
        self._build_menu()  # or just buttons
        self._build_grid()
        self._build_controls()
        self._build_status_bar()
        self._bind_keys()
        self.new_game('medium')