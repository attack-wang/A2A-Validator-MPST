class SudokuGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Sudoku")
        ...
        self.cells = [[None]*9 for _ in range(9)]
        self._build_menu()
        self._build_grid()
        self._build_controls()
        self._build_status()