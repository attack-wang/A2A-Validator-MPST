class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.board = None
        self.cell_buttons = []
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_job = None
        self.game_in_progress = False
        self._build_menu()
        self._build_status_bar()
        self.new_game("Beginner")