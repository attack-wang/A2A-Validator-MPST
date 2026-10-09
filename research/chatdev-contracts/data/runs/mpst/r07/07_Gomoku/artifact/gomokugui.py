import tkinter as tk
from board import Board
from config import (
    BOARD_SIZE, CELL_SIZE, MARGIN, CANVAS_SIZE, STONE_RADIUS, STAR_POINTS,
    PLAYER_BLACK, PLAYER_WHITE,
    COLOR_BACKGROUND, COLOR_BOARD, COLOR_GRID_LINE, COLOR_STAR_POINT,
    COLOR_LABEL, COLOR_BLACK_STONE, COLOR_BLACK_HIGHLIGHT, COLOR_WHITE_STONE,
    COLOR_WHITE_OUTLINE, COLOR_LAST_MOVE, COLOR_WIN_RING,
    COLOR_STATUS_BLACK, COLOR_STATUS_WHITE, COLOR_STATUS_WIN,
    COLOR_BUTTON_BG, COLOR_BUTTON_FG, COLOR_BUTTON_ACTIVE,
    FONT_STATUS, FONT_BUTTON, FONT_COORDINATE,
    WINDOW_TITLE, CLICK_TOLERANCE,
)
COLUMN_LABELS = "ABCDEFGHIJKLMNO"
class GomokuGUI:
    '''Tkinter window that visualises a Board and handles player input.'''
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self._setup_window()
        self._setup_widgets()
        self.redraw()
    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    def _setup_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BACKGROUND)
    def _setup_widgets(self):
        # --- Board canvas ------------------------------------------------
        self.canvas = tk.Canvas(
            self.root, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg=COLOR_BOARD, highlightthickness=0)
        self.canvas.pack(padx=12, pady=(12, 6))
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        # --- Status bar --------------------------------------------------
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var,
            font=FONT_STATUS, bg=COLOR_BACKGROUND, fg=COLOR_STATUS_BLACK)
        self.status_label.pack(pady=(0, 6))
        # --- Control buttons ---------------------------------------------
        button_bar = tk.Frame(self.root, bg=COLOR_BACKGROUND)
        button_bar.pack(pady=(0, 12))
        self.new_game_button = tk.Button(
            button_bar, text="New Game", command=self.new_game,
            font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg=COLOR_BUTTON_FG,
            activebackground=COLOR_BUTTON_ACTIVE, activeforeground=COLOR_BUTTON_FG,
            relief="flat", padx=14, pady=4, cursor="hand2")
        self.new_game_button.pack(side="left", padx=6)
        self.undo_button = tk.Button(
            button_bar, text="Undo", command=self.undo_move,
            font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg=COLOR_BUTTON_FG,
            activebackground=COLOR_BUTTON_ACTIVE, activeforeground=COLOR_BUTTON_FG,
            relief="flat", padx=14, pady=4, cursor="hand2")
        self.undo_button.pack(side="left", padx=6)
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def redraw(self):
        '''Erase the canvas and repaint board, stones and overlays.'''
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_all_stones()
        self._draw_last_move_marker()
        self._draw_winning_line()
        self._update_status()
    def _draw_grid(self):
        '''Wooden background, grid lines, star points and coordinates.'''
        # Grid lines.
        for i in range(BOARD_SIZE):
            pixel = MARGIN + i * CELL_SIZE
            # Horizontal line.
            self.canvas.create_line(
                MARGIN, pixel, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, pixel,
                fill=COLOR_GRID_LINE, width=1)
            # Vertical line.
            self.canvas.create_line(
                pixel, MARGIN, pixel, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE,
                fill=COLOR_GRID_LINE, width=1)
        # Outer border slightly thicker for a polished look.
        edge = MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
        self.canvas.create_rectangle(
            MARGIN, MARGIN, edge, edge,
            outline=COLOR_GRID_LINE, width=2)
        # Star points (hoshi).
        for row, col in STAR_POINTS:
            cx, cy = self._intersection_to_pixel(row, col)
            r = 3
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=COLOR_STAR_POINT, outline=COLOR_STAR_POINT)
        # Coordinate labels: letters on top, numbers on the left.
        for col in range(BOARD_SIZE):
            cx = MARGIN + col * CELL_SIZE
            self.canvas.create_text(
                cx, MARGIN - 18, text=COLUMN_LABELS[col],
                font=FONT_COORDINATE, fill=COLOR_LABEL)
        for row in range(BOARD_SIZE):
            cy = MARGIN + row * CELL_SIZE
            self.canvas.create_text(
                MARGIN - 18, cy, text=str(row + 1),
                font=FONT_COORDINATE, fill=COLOR_LABEL)
    def _draw_all_stones(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                player = self.board.grid[row][col]
                if player != 0:  # EMPTY
                    self._draw_stone(row, col, player)
    def _draw_stone(self, row, col, player):
        cx, cy = self._intersection_to_pixel(row, col)
        r = STONE_RADIUS
        if player == PLAYER_BLACK:
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=COLOR_BLACK_STONE, outline=COLOR_BLACK_STONE)
            # Small shine to give the stone a 3D feel.
            self.canvas.create_oval(
                cx - r // 2, cy - r + 4, cx - 2, cy - 2,
                fill=COLOR_BLACK_HIGHLIGHT, outline="")
        else:
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=COLOR_WHITE_STONE, outline=COLOR_WHITE_OUTLINE, width=1)
    def _draw_last_move_marker(self):
        '''Small red dot on the most recently placed stone.'''
        last = self.board.last_move()
        if last is None:
            return
        row, col, _player = last
        cx, cy = self._intersection_to_pixel(row, col)
        r = 4
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=COLOR_LAST_MOVE, outline=COLOR_LAST_MOVE)
    def _draw_winning_line(self):
        '''Red rings around every stone that is part of the winning line.'''
        if not self.board.winning_line:
            return
        r = STONE_RADIUS + 3
        for row, col in self.board.winning_line:
            cx, cy = self._intersection_to_pixel(row, col)
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=COLOR_WIN_RING, width=3)