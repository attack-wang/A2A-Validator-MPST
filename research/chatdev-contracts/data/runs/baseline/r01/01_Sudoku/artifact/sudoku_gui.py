'''
sudoku_gui.py
Tkinter graphical interface for the Sudoku game: renders the 9x9 grid,
handles mouse/keyboard input, highlights mistakes and shows a completion
dialog when the puzzle is solved.
'''
import random
import tkinter as tk
from tkinter import messagebox, ttk
from puzzle_generator import PuzzleGenerator
from sudoku_board import SudokuBoard
CELL_SIZE = 60
BOARD_PIXELS = CELL_SIZE * 9
MARGIN = 30
WINDOW_SIZE = BOARD_PIXELS + MARGIN * 2
DIFFICULTIES = ("easy", "medium", "hard")
class SudokuGUI:
    """Main application window for the Sudoku game."""
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        # Game state
        self.rng = random.Random()
        self.board = None
        self.solution = None
        self.selected = None
        self.conflicts = set()
        self.game_over = False
        self.elapsed_seconds = 0
        self.timer_running = False
        self._closing = False
        self._tick_scheduled = False
        # Canvas for the board
        self.canvas = tk.Canvas(root, width=WINDOW_SIZE,
                                height=BOARD_PIXELS + MARGIN * 2,
                                bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=(10, 5))
        self.canvas.bind("<Button-1>", self._on_click)
        # Allow the canvas to receive keyboard events
        self.canvas.focus_set()
        # Control panel
        control_frame = tk.Frame(root)
        control_frame.pack(pady=(0, 5))
        tk.Label(control_frame, text="Difficulty:").pack(side=tk.LEFT, padx=(0, 4))
        self.difficulty_var = tk.StringVar(value="medium")
        for level in DIFFICULTIES:
            tk.Radiobutton(control_frame, text=level.title(),
                           variable=self.difficulty_var, value=level
                           ).pack(side=tk.LEFT)
        tk.Button(control_frame, text="New Game",
                  command=self._new_game).pack(side=tk.LEFT, padx=(8, 4))
        tk.Button(control_frame, text="Hint",
                  command=self.give_hint).pack(side=tk.LEFT, padx=4)
        tk.Button(control_frame, text="Check",
                  command=self.check_board).pack(side=tk.LEFT, padx=4)
        # Status bar
        self.status_var = tk.StringVar(value="Press New Game to start.")
        status_bar = tk.Frame(root)
        status_bar.pack(fill=tk.X, pady=(0, 10))
        tk.Label(status_bar, textvariable=self.status_var, anchor="w"
                 ).pack(side=tk.LEFT, padx=8)
        self.timer_label = tk.Label(status_bar, text="Time: 00:00")
        self.timer_label.pack(side=tk.RIGHT, padx=8)
        # Keyboard bindings
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Left>", lambda e: self._move_selection(0, -1))
        self.root.bind("<Right>", lambda e: self._move_selection(0, 1))
        self.root.bind("<Up>", lambda e: self._move_selection(-1, 0))
        self.root.bind("<Down>", lambda e: self._move_selection(1, 0))
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        # Start with a fresh puzzle
        self._new_game()
    # ------------------------------------------------------------------
    # Game setup
    # ------------------------------------------------------------------
    def _new_game(self):
        generator = PuzzleGenerator(seed=self.rng.randint(0, 10 ** 9))
        puzzle, solution = generator.generate(self.difficulty_var.get())
        self.board = SudokuBoard(puzzle)
        self.solution = [list(row) for row in solution]
        self.selected = None
        self.game_over = False
        self.elapsed_seconds = 0
        self._update_timer_label()
        if not self.timer_running:
            self._start_timer()
        self._after_move(solved_message=False)
        self._set_status("New %s puzzle started. Good luck!"
                         % self.difficulty_var.get().title())