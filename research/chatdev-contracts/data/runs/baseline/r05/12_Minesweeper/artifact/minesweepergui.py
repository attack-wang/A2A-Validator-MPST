class MinesweeperGUI:
    '''Tkinter front-end for the Minesweeper game.'''
    CELL_SIZE_BY_DIFFICULTY = {"Beginner": 30, "Intermediate": 26, "Expert": 22}
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.game = MinesweeperGame("Beginner")
        self.cell_buttons = []
        self.timer_job = None
        self._build_menu()
        self._build_header()
        self._build_board()
        self._refresh_all_cells()
        self._update_header()