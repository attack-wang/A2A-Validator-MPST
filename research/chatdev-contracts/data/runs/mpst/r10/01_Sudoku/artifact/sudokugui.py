class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Classic Sudoku")
        self.master.resizable(False, False)
        self.generator = SudokuGenerator()
        self.board = None
        self.cells = [[None]*9 for _ in range(9)]  # tk.Entry widgets
        self.selected = None  # (row, col)
        self.mistakes = 0
        self.start_time = None
        self.timer_running = False
        self.solved = False
        self._build_menu()
        self._build_header()
        self._build_grid()
        self._build_controls()
        self._build_status_bar()
        self._new_game("Medium")