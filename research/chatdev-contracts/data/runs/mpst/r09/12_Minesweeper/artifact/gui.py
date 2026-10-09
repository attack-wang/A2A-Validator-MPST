'''
Tkinter graphical interface for the Minesweeper game.
Renders the board as a grid of buttons, handles left-click (reveal /
chord) and right-click (flag) input, keeps the mine counter and timer
up to date, and offers a difficulty menu plus a smiley reset button.
'''
import tkinter as tk
from tkinter import messagebox
import config
from board import Board, STATUS_PLAYING, STATUS_WON, STATUS_LOST
class MinesweeperGUI:
    """Main application window: menu, header (counter/face/timer) and board."""
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.difficulty = config.DEFAULT_DIFFICULTY
        self.board = Board(self.difficulty.rows, self.difficulty.cols,
                           self.difficulty.mines)
        self.cell_buttons = []
        self.board_frame = None
        self.elapsed_seconds = 0
        self.timer_job = None
        self.timer_running = False  # was missing -> AttributeError; now initialized
        self.game_finished = False
        self._build_menu()
        self._build_header()
        self._build_board()
        self._update_display()
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_menu(self):
        """Build the menu bar with the three difficulty presets and reset."""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        for level in config.DIFFICULTY_LEVELS:
            game_menu.add_command(
                label="{} ({}x{}, {} mines)".format(
                    level.name, level.rows, level.cols, level.mines),
                command=lambda lvl=level: self._change_difficulty(lvl))
        game_menu.add_separator()
        game_menu.add_command(label="New Game", command=self._reset_game)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
    def _build_header(self):
        """Build the header row: mine counter, smiley reset button, timer."""
        header = tk.Frame(self.root, bg=config.COLOR_HEADER_BG,
                          padx=10, pady=6)
        header.pack(fill=tk.BOTH)
        self.mine_label = tk.Label(header, text="", font=config.FONT_HEADER,
                                   bg=config.COLOR_HEADER_BG, fg="#B71C1C")
        self.mine_label.pack(side=tk.LEFT)
        self.face_button = tk.Button(header, text=config.FACE_PLAYING,
                                     font=config.FONT_HEADER,
                                     bg=config.COLOR_HEADER_BG,
                                     relief=tk.RAISED, padx=8,
                                     command=self._reset_game)
        self.face_button.pack(side=tk.LEFT, expand=True)
        self.timer_label = tk.Label(header, text="000", font=config.FONT_HEADER,
                                    bg=config.COLOR_HEADER_BG, fg="#B71C1C")
        self.timer_label.pack(side=tk.RIGHT)
    def _build_board(self):
        """Build the grid of cell buttons for the current difficulty."""
        self.board_frame = tk.Frame(self.root, bg=config.COLOR_BG,
                                    padx=4, pady=4)
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        self.cell_buttons = []
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                btn = tk.Button(self.board_frame, text="", width=2, height=1,
                                font=config.FONT_CELL,
                                bg=config.COLOR_UNREVEALED,
                                relief=tk.RAISED)
                btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                # Left click: reveal (or chord on a revealed number).
                btn.bind("<Button-1>",
                         lambda event, rr=r, cc=c: self._on_left_click(rr, cc))
                # Right click: toggle flag (Button-3 on Windows/Linux,
                # Button-2 on macOS).
                btn.bind("<Button-3>",
                         lambda event, rr=r, cc=c: self._on_right_click(rr, cc))
                btn.bind("<Button-2>",
                         lambda event, rr=r, cc=c: self._on_right_click(rr, cc))
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)
    def _rebuild_board(self):
        """Destroy the old board widgets and build new ones (difficulty change)."""
        if self.board_frame is not None:
            self.board_frame.destroy()
        self._build_board()