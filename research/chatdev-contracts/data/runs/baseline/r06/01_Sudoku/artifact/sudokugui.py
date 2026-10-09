import tkinter as tk
from tkinter import messagebox
from sudoku_board import SudokuBoard
from sudoku_generator import SudokuGenerator
class SudokuGUI:
    """Tkinter window that renders the board and handles all player interaction."""
    CELL_SIZE = 60
    BOARD_SIZE = CELL_SIZE * 9
    MARGIN = 24
    # Colors
    BG_COLOR = "#f7f3e9"
    LINE_COLOR = "#8a8a8a"
    THICK_LINE_COLOR = "#222222"
    FIXED_CELL_BG = "#e6e2d3"
    USER_CELL_BG = "#ffffff"
    EMPTY_CELL_BG = "#ffffff"
    SELECTED_BG = "#bcd4f5"
    PEER_BG = "#eef3fb"
    CONFLICT_BG = "#f5a9a2"
    FIXED_TEXT = "#404040"
    USER_TEXT = "#1a5fb4"
    ERROR_TEXT = "#b3261e"
    def __init__(self, root, difficulty="medium"):
        self.root = root
        self.difficulty = difficulty
        self.board = SudokuBoard()
        self.generator = SudokuGenerator()
        self.solution = None
        self.selected = None  # (row, col) or None
        self.show_mistakes = tk.BooleanVar(value=True)
        root.title("Sudoku - ChatDev")
        root.resizable(False, False)
        root.configure(bg=self.BG_COLOR)
        self._build_menu()
        self.canvas = tk.Canvas(
            root,
            width=self.BOARD_SIZE + 2 * self.MARGIN,
            height=self.BOARD_SIZE + 2 * self.MARGIN,
            bg=self.BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self._build_controls()
        root.bind("<Key>", self.on_key_press)
        root.bind("<Up>", lambda e: self.move_selection(-1, 0))
        root.bind("<Down>", lambda e: self.move_selection(1, 0))
        root.bind("<Left>", lambda e: self.move_selection(0, -1))
        root.bind("<Right>", lambda e: self.move_selection(0, 1))
        self.new_game(difficulty)