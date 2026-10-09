'''
mastermindgui.py
Graphical user interface for the Mastermind game, built with tkinter.
Renders the hidden secret row, the guess history with exact/partial
feedback pegs, a clickable color palette, and clear win/lose dialogs.
'''
import tkinter as tk
from tkinter import messagebox
from game import MastermindGame
# Visual mapping from color names to hex values.
COLOR_HEX = {
    'red': '#e53935',
    'blue': '#1e88e5',
    'green': '#43a047',
    'yellow': '#fdd835',
    'orange': '#fb8c00',
    'purple': '#8e24aa',
    'pink': '#ec407a',
    'brown': '#6d4c41',
}
BG_COLOR = '#2b2b2b'
PANEL_COLOR = '#3c3f41'
TEXT_FG = '#eeeeee'
STATUS_WARN = '#ffb74d'
STATUS_OK = '#81c784'
STATUS_INFO = '#90caf9'
class MastermindGUI:
    """Tkinter front-end that drives one MastermindGame instance."""
    PEG_RADIUS = 18          # radius of a guess peg, in pixels
    FEEDBACK_RADIUS = 7      # radius of a feedback peg, in pixels
    FEEDBACK_SPACING = 18    # vertical spacing between feedback pegs
    PEG_FONT = ('Helvetica', 14, 'bold')
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind - Code Breaker")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        self.game = MastermindGame()
        self.current_guess = []
        self.history_items = []  # canvas item ids, for cleanup on reset
        self._compute_layout_metrics()
        self._build_widgets()
        self._reset_board()
    # ------------------------------------------------------------------
    # Layout metrics
    # ------------------------------------------------------------------
    def _compute_layout_metrics(self):
        """Pre-compute pixel geometry so every row is drawn consistently."""
        self.palette = self.game.get_palette()
        self.board_width = 560
        # Row height must fit both the pegs and the stacked feedback pegs.
        feedback_rows = (self.game.code_length + 1) // 2
        self.row_height = max(
            self.PEG_RADIUS * 2 + 20,
            feedback_rows * self.FEEDBACK_SPACING + 2 * self.FEEDBACK_RADIUS + 12,
        )
        self.peg_start_x = 70
        self.peg_spacing = 2 * self.PEG_RADIUS + 14
        self.feedback_x = (self.peg_start_x
                           + self.game.code_length * self.peg_spacing + 30)
        self.board_visible_height = min(6 * self.row_height, 480)
    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------
    def _build_widgets(self):
        """Create header, board, palette, controls and status bar."""
        # --- Header ---------------------------------------------------
        header = tk.Label(
            self.root, text="MASTERMIND", font=('Helvetica', 18, 'bold'),
            fg=TEXT_FG, bg=BG_COLOR)
        header.pack(pady=(10, 2))
        subtitle = tk.Label(
            self.root,
            text="Crack the hidden code of {} colors in {} tries!".format(
                self.game.code_length, self.game.max_attempts),
            font=('Helvetica', 10), fg=STATUS_INFO, bg=BG_COLOR)
        subtitle.pack(pady=(0, 8))
        # --- Board canvas with scrollbar ------------------------------
        board_frame = tk.Frame(self.root, bg=BG_COLOR)
        board_frame.pack(padx=10, pady=4)
        self.board_canvas = tk.Canvas(
            board_frame, width=self.board_width,
            height=self.board_visible_height,
            bg=PANEL_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(board_frame, orient='vertical',
                                 command=self.board_canvas.yview)
        self.board_canvas.configure(yscrollcommand=scrollbar.set)
        self.board_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        # --- Current guess row ----------------------------------------
        self.guess_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.guess_frame.pack(pady=6)
        self.guess_canvas = tk.Canvas(
            self.guess_frame, width=self.board_width,
            height=self.PEG_RADIUS * 2 + 8,
            bg=BG_COLOR, highlightthickness=0)
        self.guess_canvas.pack()
        # --- Palette ---------------------------------------------------
        palette_frame = tk.Frame(self.root, bg=BG_COLOR)
        palette_frame.pack(pady=4)
        for color in self.palette:
            btn = tk.Button(
                palette_frame, text=color.capitalize(),
                bg=COLOR_HEX.get(color, '#888888'),
                fg='white' if color in ('brown', 'blue', 'purple', 'red') else 'black',
                activebackground=COLOR_HEX.get(color, '#888888'),
                font=('Helvetica', 10, 'bold'), width=8, relief='raised',
                command=lambda c=color: self._on_palette_click(c))
            btn.pack(side='left', padx=4)
        # --- Controls ---------------------------------------------------
        controls_frame = tk.Frame(self.root, bg=BG_COLOR)
        controls_frame.pack(pady=6)
        tk.Button(controls_frame, text='Submit Guess', width=14,
                  font=('Helvetica', 10, 'bold'),
                  command=self._submit_guess).pack(side='left', padx=6)
        tk.Button(controls_frame, text='Clear', width=8,
                  command=self._clear_guess).pack(side='left', padx=6)
        tk.Button(controls_frame, text='New Game', width=10,
                  command=self._new_game).pack(side='left', padx=6)
        # --- Attempts + status bar --------------------------------------
        self.attempts_label = tk.Label(
            self.root, text='', font=('Helvetica', 10, 'bold'),
            fg=TEXT_FG, bg=BG_COLOR)
        self.attempts_label.pack(pady=(4, 0))
        self.status_label = tk.Label(
            self.root, text='Welcome! Pick colors to build your first guess.',
            font=('Helvetica', 10), fg=STATUS_INFO, bg=BG_COLOR,
            wraplength=self.board_width, justify='center')
        self.status_label.pack(pady=(0, 10), padx=10, fill='x')