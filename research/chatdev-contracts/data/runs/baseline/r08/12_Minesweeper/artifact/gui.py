'''
gui.py
Graphical user interface for the Minesweeper game.
Implements the GameGUI class: difficulty menu, status bar (mine counter,
reset button, timer), board grid with left-click reveal and right-click
flagging, distinct visuals for flagged cells, and win/lose handling.
'''
import tkinter as tk
from tkinter import messagebox
from config import (DIFFICULTY_LEVELS, BEGINNER, NUMBER_COLORS,
                    UNREVEALED_BG, REVEALED_BG, FLAGGED_BG, MINE_BG,
                    WRONG_FLAG_BG, STATUS_BG, COUNTER_BG, COUNTER_FG,
                    CELL_FONT, STATUS_FONT, FACE_FONT)
from game_logic import Board
class GameGUI:
    """Tkinter front-end for the Minesweeper board."""
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.root.configure(bg=STATUS_BG)
        self.difficulty = BEGINNER
        self.board = None
        self.buttons = []
        self._timer_job = None
        self.elapsed_time = 0
        self._game_id = 0
        self._build_menu()
        self._build_status_bar()
        self._build_board_frame()
        self._new_game(BEGINNER)
        self._center_window()
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_menu(self):
        """Create the menu bar with a New Game command and difficulty radio buttons."""
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self._reset_current)
        game_menu.add_separator()
        self._difficulty_var = tk.StringVar(value=self.difficulty.name)
        for level in DIFFICULTY_LEVELS:
            game_menu.add_radiobutton(
                label=f"{level.name} ({level.rows}x{level.cols}, {level.mines} mines)",
                variable=self._difficulty_var,
                value=level.name,
                command=lambda lvl=level: self._new_game(lvl),
            )
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)
    def _build_status_bar(self):
        """Create the status bar: mine counter, reset button, timer."""
        self.status_frame = tk.Frame(self.root, bd=3, relief=tk.GROOVE, bg=STATUS_BG)
        self.status_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        self.mine_counter = tk.Label(
            self.status_frame, text="010", font=STATUS_FONT,
            fg=COUNTER_FG, bg=COUNTER_BG, width=3, padx=4,
        )
        self.mine_counter.pack(side="left", padx=8, pady=4)
        self.reset_button = tk.Button(
            self.status_frame, text="🙂", font=FACE_FONT, width=3,
            bg=STATUS_BG, relief=tk.RAISED, command=self._reset_current,
        )
        self.reset_button.pack(side="left", expand=True)
        self.timer_label = tk.Label(
            self.status_frame, text="000", font=STATUS_FONT,
            fg=COUNTER_FG, bg=COUNTER_BG, width=3, padx=4,
        )
        self.timer_label.pack(side="right", padx=8, pady=4)
    def _build_board_frame(self):
        """Create the frame that will hold the grid of cell buttons."""
        self.board_frame = tk.Frame(self.root, bd=3, relief=tk.GROOVE, bg=STATUS_BG)
        self.board_frame.grid(row=1, column=0, padx=5, pady=5)
    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------
    def _new_game(self, difficulty):
        """Start a fresh game with the given difficulty."""
        self._stop_timer()
        self._game_id += 1
        self.difficulty = difficulty
        self.board = Board(difficulty.rows, difficulty.cols, difficulty.mines)
        self.elapsed_time = 0
        self._timer_job = None
        self._update_counter()
        self._update_timer_display()
        self.reset_button.config(text="🙂")
        self._build_grid()
        self._refresh_board()
    def _reset_current(self):
        """Restart the current difficulty."""
        self._new_game(self.difficulty)
    def _build_grid(self):
        """(Re)build the grid of cell buttons for the current board size."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        for r in range(self.board.rows):
            row_buttons = []
            for c in range(self.board.cols):
                btn = tk.Button(
                    self.board_frame, width=2, height=1,
                    font=CELL_FONT, bg=UNREVEALED_BG, relief=tk.RAISED,
                )
                btn.grid(row=r, column=c, padx=0, pady=0, sticky="nsew")
                btn.bind("<Button-1>", lambda event, rr=r, cc=c: self._on_left_click(rr, cc))
                btn.bind("<Button-3>", lambda event, rr=r, cc=c: self._on_right_click(rr, cc))
                # macOS: right-click is Button-2
                btn.bind("<Button-2>", lambda event, rr=r, cc=c: self._on_right_click(rr, cc))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------
    def _on_left_click(self, row, col):
        """Left click: uncover the cell (starts timer on first move)."""
        if self.board.game_over:
            return
        if not self.board.mines_placed:
            self._start_timer()
        result = self.board.reveal_cell(row, col)
        if result == "mine":
            self.board.reveal_all_mines()
            self._end_game(won=False)
        else:
            if self.board.game_over and self.board.won:
                self._end_game(won=True)
            else:
                self._refresh_board()
    def _on_right_click(self, row, col):
        """Right click: toggle a flag on the cell."""
        if self.board.game_over:
            return
        self.board.toggle_flag(row, col)
        self._update_counter()
        self._refresh_board()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _refresh_board(self):
        """Redraw every cell button according to the board state."""
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.get_cell(r, c)
                btn = self.buttons[r][c]
                if cell.is_revealed:
                    if cell.is_mine:
                        btn.config(text="💣", bg=MINE_BG, relief=tk.FLAT)
                    elif cell.adjacent_mines > 0:
                        btn.config(
                            text=str(cell.adjacent_mines),
                            bg=REVEALED_BG, relief=tk.FLAT,
                            fg=NUMBER_COLORS.get(cell.adjacent_mines, "#000000"),
                        )
                    else:
                        btn.config(text="", bg=REVEALED_BG, relief=tk.FLAT)
                elif self.board.game_over and cell.is_flagged and not cell.is_mine:
                    # Wrongly flagged cell, shown only after a loss
                    btn.config(text="❌", bg=WRONG_FLAG_BG, relief=tk.FLAT)
                elif cell.is_flagged:
                    # Distinct visual for flagged cells
                    btn.config(text="🚩", bg=FLAGGED_BG, relief=tk.RAISED)
                else:
                    btn.config(text="", bg=UNREVEALED_BG, relief=tk.RAISED)
    def _update_counter(self):
        """Show remaining mines (mines minus flags), zero-padded to 3 digits."""
        remaining = max(self.board.remaining_mines(), -99)
        self.mine_counter.config(text=f"{remaining:03d}" if remaining >= 0 else f"-{abs(remaining):02d}")
    def _update_timer_display(self):
        """Show elapsed seconds, zero-padded to 3 digits."""
        self.timer_label.config(text=f"{min(self.elapsed_time, 999):03d}")
    # ------------------------------------------------------------------
    # Timer
    # ------------------------------------------------------------------
    def _start_timer(self):
        """Start the per-second timer tick."""
        if self._timer_job is None:
            self._tick()
    def _tick(self):
        """One timer tick: increment elapsed time and reschedule."""
        self.elapsed_time += 1
        self._update_timer_display()
        self._timer_job = self.root.after(1000, self._tick)
    def _stop_timer(self):
        """Cancel the timer tick if it is running."""
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None
    # ------------------------------------------------------------------
    # End of game
    # ------------------------------------------------------------------
    def _end_game(self, won):
        """Stop the timer, refresh the board, set the face, announce the result."""
        self._stop_timer()
        self._refresh_board()
        self.reset_button.config(text="😎" if won else "😵")
        game_id = self._game_id
        self.root.after(400, lambda: self._announce_result(won, game_id))
    def _announce_result(self, won, game_id):
        """Show the win/lose dialog unless a new game already started."""
        if game_id != self._game_id:
            return
        if won:
            messagebox.showinfo("Minesweeper", f"🎉 You cleared the field in {self.elapsed_time} seconds!")
        else:
            messagebox.showerror("Minesweeper", "💥 Boom! You hit a mine. Better luck next time!")
    # ------------------------------------------------------------------
    # Window helpers
    # ------------------------------------------------------------------
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")