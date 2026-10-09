"""
gui.py
Tkinter front-end for the Minesweeper game.
Wires the Board logic to a clickable cell grid, handles left/right/middle
mouse actions, flagging visuals, the timer, the mine counter and the
smiley status button.
"""
import tkinter as tk
from tkinter import messagebox
import config
from board import Board
class MinesweeperGUI:
    """Main window: menu, status bar, cell grid and event handling."""
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper - ChatDev Edition")
        self.root.resizable(False, False)
        self.difficulty_name = config.DEFAULT_DIFFICULTY
        self.board = None
        self.buttons = []
        self.timer_job = None
        self.elapsed_seconds = 0
        self.timer_running = False
        self._build_menu()
        self._build_status_bar()
        self._build_board_area()
        self.new_game(self.difficulty_name)
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_menu(self):
        """Create the menu bar (Game / Help) and the F2 shortcut."""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", accelerator="F2",
                              command=lambda: self.new_game(self.difficulty_name))
        game_menu.add_separator()
        self._difficulty_var = tk.StringVar(value=self.difficulty_name)
        for name in config.DIFFICULTIES:
            game_menu.add_radiobutton(label=name, value=name,
                                      variable=self._difficulty_var,
                                      command=lambda: self.new_game(self._difficulty_var.get()))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to play", command=self._show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)
        self.root.bind("<F2>", lambda e: self.new_game(self.difficulty_name))
    def _build_status_bar(self):
        """Create the mine counter, smiley reset button and timer display."""
        bar = tk.Frame(self.root, bg=config.COLOR_STATUS_BG, padx=8, pady=6)
        bar.pack(fill=tk.X, side=tk.TOP)
        self.mine_label = tk.Label(bar, text="010", font=config.FONT_STATUS,
                                   bg="#000000", fg="#FF5555", width=5, pady=2,
                                   relief=tk.GROOVE)
        self.mine_label.pack(side=tk.LEFT)
        self.smiley_button = tk.Button(bar, text=config.SMILE_PLAYING,
                                       font=(config.FONT_FAMILY, 14),
                                       width=3, relief=tk.RAISED,
                                       command=self._restart)
        self.smiley_button.pack(side=tk.LEFT, expand=True, padx=20)
        self.time_label = tk.Label(bar, text="000", font=config.FONT_STATUS,
                                   bg="#000000", fg="#FF5555", width=5, pady=2,
                                   relief=tk.GROOVE)
        self.time_label.pack(side=tk.RIGHT)
    def _build_board_area(self):
        """Create the container frame that hosts the cell grid."""
        self.board_frame = tk.Frame(self.root, bg=config.COLOR_BOARD_BG,
                                    padx=6, pady=6)
        self.board_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
    def _build_cell_grid(self):
        """(Re)create the clickable cell buttons for the current board."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                btn = tk.Button(self.board_frame, text="", width=3, height=1,
                                font=config.FONT_CELL, relief=tk.RAISED,
                                bg=config.COLOR_HIDDEN,
                                activebackground=config.COLOR_HIDDEN_ACTIVE,
                                highlightthickness=0, bd=1)
                btn.grid(row=r, column=c, padx=0, pady=0, sticky="nsew")
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self._on_left_click(rr, cc))
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self._on_right_click(rr, cc))
                btn.bind("<Button-2>", lambda e, rr=r, cc=c: self._on_chord(rr, cc))
                btn.bind("<Enter>", lambda e, rr=r, cc=c: self._on_hover(rr, cc))
                btn.bind("<Leave>", lambda e: self._on_hover_end())
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def new_game(self, difficulty_name):
        """Start a fresh game with the selected difficulty."""
        if difficulty_name not in config.DIFFICULTIES:
            difficulty_name = config.DEFAULT_DIFFICULTY
        rows, cols, mines = config.DIFFICULTIES[difficulty_name]
        self.difficulty_name = difficulty_name
        self._stop_timer()
        self.elapsed_seconds = 0
        self.board = Board(rows, cols, mines)
        self._build_cell_grid()
        self.smiley_button.config(text=config.SMILE_PLAYING)
        self._update_status_bar()
    def _restart(self):
        """Smiley button callback: replay the same difficulty."""
        self.new_game(self.difficulty_name)
    def _show_help(self):
        """Show a short instructions dialog."""
        messagebox.showinfo(
            "How to play",
            "• Left click: uncover a cell\n"
            "• Right click: place / remove a flag 🚩\n"
            "• Middle click on a revealed number: reveal its neighbours\n"
            "  when the adjacent flag count matches the number (chording)\n\n"
            "Numbers show how many mines touch that cell.\n"
            "Uncover every safe cell to win — hit a mine and you lose!"
        )
    # ------------------------------------------------------------------
    # Mouse event handlers
    # ------------------------------------------------------------------
    def _on_left_click(self, row, col):
        """Uncover the clicked cell and refresh the board."""
        if self.board.game_over:
            return
        revealed = self.board.reveal_cell(row, col)
        if revealed:
            self._start_timer()
            self._refresh_board()
            self._update_status_bar()
            self._handle_game_end()
    def _on_right_click(self, row, col):
        """Toggle a flag on the clicked cell and refresh it."""
        if self.board.game_over:
            return
        if self.board.toggle_flag(row, col):
            self._start_timer()
            self._refresh_cell(row, col)
            self._update_status_bar()
    def _on_chord(self, row, col):
        """Middle click on a revealed number: chord its neighbours."""
        if self.board.game_over:
            return
        revealed = self.board.chord(row, col)
        if revealed:
            self._start_timer()
            self._refresh_board()
            self._update_status_bar()
            self._handle_game_end()
    def _on_hover(self, row, col):
        """Show the 'oh' face while the pointer is over a hidden cell."""
        if self.board.game_over:
            return
        if not self.board.cell(row, col).is_revealed:
            self.smiley_button.config(text=config.SMILE_OH)
    def _on_hover_end(self):
        """Restore the normal face when the pointer leaves a cell."""
        if not self.board.game_over:
            self.smiley_button.config(text=config.SMILE_PLAYING)
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _refresh_board(self):
        """Redraw every cell of the board."""
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                self._refresh_cell(r, c)
    def _refresh_cell(self, r, c):
        """Update the visual state of a single cell button."""
        cell = self.board.cell(r, c)
        btn = self.buttons[r][c]
        if cell.is_revealed:
            if cell.is_mine:
                # The mine that exploded gets a red background.
                bg = (config.COLOR_MINE_BG
                      if self.board.exploded_cell == (r, c)
                      else config.COLOR_MINE_REVEALED)
                btn.config(text=config.SYMBOL_MINE, bg=bg, relief=tk.FLAT)
            else:
                n = cell.adjacent_mines
                btn.config(text=str(n) if n else "",
                           bg=config.COLOR_REVEALED, relief=tk.FLAT,
                           fg=config.NUMBER_COLORS.get(n, "#000000"))
        elif cell.is_flagged:
            if self.board.game_over and not self.board.won and not cell.is_mine:
                # A flag placed on a safe cell: mark it as wrong.
                btn.config(text=config.SYMBOL_WRONG,
                           bg=config.COLOR_WRONG_FLAG_BG, relief=tk.FLAT)
            else:
                btn.config(text=config.SYMBOL_FLAG,
                           bg=config.COLOR_FLAGGED, relief=tk.RAISED)
        else:
            btn.config(text="", bg=config.COLOR_HIDDEN, relief=tk.RAISED,
                       fg="#000000")
    def _handle_game_end(self):
        """Stop the timer, disclose mines and announce the outcome."""
        if not self.board.game_over:
            return
        self._stop_timer()
        if self.board.won:
            # Flag every mine so the finished board looks complete.
            for row in self.board.grid:
                for cell in row:
                    if cell.is_mine:
                        cell.is_flagged = True
            self.smiley_button.config(text=config.SMILE_WIN)
            self._refresh_board()
            self._update_status_bar()
            messagebox.showinfo("Minesweeper", "You cleared the board — you win! 😎")
        else:
            self.board.reveal_all_mines()
            self.smiley_button.config(text=config.SMILE_LOSE)
            self._refresh_board()
            self._update_status_bar()
            messagebox.showinfo("Minesweeper", "Boom! You uncovered a mine. 💣")
    def _update_status_bar(self):
        """Refresh the mine counter and the timer display."""
        remaining = self.board.num_mines - self.board.flags_count()
        if remaining < 0:
            mine_text = "-{:02d}".format(abs(remaining))
        else:
            mine_text = "{:03d}".format(remaining)
        self.mine_label.config(text=mine_text)
        seconds = min(self.elapsed_seconds, config.MAX_TIME_SECONDS)
        self.time_label.config(text="{:03d}".format(seconds))
    # ------------------------------------------------------------------
    # Timer
    # ------------------------------------------------------------------
    def _start_timer(self):
        """Start the 1-second ticker on the first effective move."""
        if not self.timer_running:
            self.timer_running = True
            self._schedule_tick()
    def _schedule_tick(self):
        """Register the next timer callback with Tkinter."""
        self.timer_job = self.root.after(config.TIMER_INTERVAL_MS, self._tick)
    def _tick(self):
        """Increment the elapsed time and refresh the display."""
        if self.elapsed_seconds < config.MAX_TIME_SECONDS:
            self.elapsed_seconds += 1
        self._update_status_bar()
        if self.timer_running:
            self._schedule_tick()
    def _stop_timer(self):
        """Cancel any pending timer callback."""
        self.timer_running = False
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None