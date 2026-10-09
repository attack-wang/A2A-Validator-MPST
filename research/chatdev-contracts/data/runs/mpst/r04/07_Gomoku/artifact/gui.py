'''
gui.py
Defines the GomokuGUI class: a tkinter based interface that renders the
board, handles mouse clicks for stone placement, highlights the last
move and the winning line, and offers a restart button.
'''
import tkinter as tk
from constants import (BOARD_SIZE, CELL_SIZE, MARGIN, STONE_RADIUS,
                       WINDOW_WIDTH, WINDOW_HEIGHT,
                       EMPTY, BLACK, WHITE,
                       COLOR_BACKGROUND, COLOR_GRID_LINE, COLOR_STAR_POINT,
                       COLOR_BLACK_STONE, COLOR_WHITE_STONE,
                       COLOR_WHITE_STONE_EDGE,
                       COLOR_LAST_MOVE_MARK, COLOR_WIN_HIGHLIGHT,
                       COLOR_STATUS_BG, COLOR_STATUS_FG,
                       COLOR_BUTTON_BG, COLOR_BUTTON_BG_ACTIVE,
                       COLOR_BUTTON_FG)
# Intersections traditionally marked with a star point on a 15x15 board
STAR_POINTS = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
class GomokuGUI:
    '''Tkinter window that visualises the Gomoku board and handles input.'''
    def __init__(self, game):
        '''Build the window, canvas, status bar and restart button.'''
        self.game = game
        self.root = tk.Tk()
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        # Status label above the board
        self.status_label = tk.Label(
            self.root, text=self.game.get_status_message(),
            font=("Helvetica", 14, "bold"),
            bg=COLOR_STATUS_BG, fg=COLOR_STATUS_FG, pady=8,
        )
        self.status_label.pack(fill=tk.X)
        # Board canvas
        self.canvas = tk.Canvas(
            self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
            bg=COLOR_BACKGROUND, highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        # Restart button below the board
        self.restart_button = tk.Button(
            self.root, text="Restart", font=("Helvetica", 12, "bold"),
            bg=COLOR_BUTTON_BG, fg=COLOR_BUTTON_FG,
            activebackground=COLOR_BUTTON_BG_ACTIVE,
            activeforeground=COLOR_BUTTON_FG,
            relief=tk.RAISED, bd=2, command=self.restart,
        )
        self.restart_button.pack(pady=8)
        self.draw_board()
    # ------------------------------------------------------------------
    # Coordinate helpers
    # ------------------------------------------------------------------
    def board_to_pixel(self, row, col):
        '''Convert board coordinates (row, col) to canvas pixel center.'''
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        return x, y
    def pixel_to_board(self, x, y):
        '''
        Convert canvas pixel coordinates to the nearest intersection.
        Returns (row, col) or None when the click is outside the board.
        '''
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw_board(self):
        '''Draw the wooden background, grid lines and star points.'''
        self.canvas.delete("all")
        # Outer border
        x0, y0 = self.board_to_pixel(0, 0)
        x1, y1 = self.board_to_pixel(BOARD_SIZE - 1, BOARD_SIZE - 1)
        self.canvas.create_rectangle(
            x0 - 3, y0 - 3, x1 + 3, y1 + 3,
            outline=COLOR_GRID_LINE, width=2,
        )
        # Grid lines
        for i in range(BOARD_SIZE):
            x_start, y_start = self.board_to_pixel(i, 0)
            x_end, y_end = self.board_to_pixel(i, BOARD_SIZE - 1)
            self.canvas.create_line(
                x_start, y_start, x_end, y_end,
                fill=COLOR_GRID_LINE, width=1,
            )
            x_start, y_start = self.board_to_pixel(0, i)
            x_end, y_end = self.board_to_pixel(BOARD_SIZE - 1, i)
            self.canvas.create_line(
                x_start, y_start, x_end, y_end,
                fill=COLOR_GRID_LINE, width=1,
            )
        # Star points
        for row, col in STAR_POINTS:
            x, y = self.board_to_pixel(row, col)
            self.canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4,
                fill=COLOR_STAR_POINT, outline=COLOR_STAR_POINT,
            )
        # Stones
        self.draw_stones()
    def draw_stones(self):
        '''Draw every stone currently on the board, plus markers.'''
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                stone = self.game.board.get_stone(row, col)
                if stone == EMPTY:
                    continue
                x, y = self.board_to_pixel(row, col)
                fill = COLOR_BLACK_STONE if stone == BLACK else COLOR_WHITE_STONE
                outline = (COLOR_BLACK_STONE if stone == BLACK
                           else COLOR_WHITE_STONE_EDGE)
                self.canvas.create_oval(
                    x - STONE_RADIUS, y - STONE_RADIUS,
                    x + STONE_RADIUS, y + STONE_RADIUS,
                    fill=fill, outline=outline, width=1,
                )
        # Highlight the winning line, if any
        if self.game.winning_line:
            for row, col in self.game.winning_line:
                x, y = self.board_to_pixel(row, col)
                self.canvas.create_oval(
                    x - STONE_RADIUS - 3, y - STONE_RADIUS - 3,
                    x + STONE_RADIUS + 3, y + STONE_RADIUS + 3,
                    outline=COLOR_WIN_HIGHLIGHT, width=3,
                )
        # Mark the most recent move
        if self.game.last_move:
            row, col = self.game.last_move
            x, y = self.board_to_pixel(row, col)
            mark = 5
            self.canvas.create_line(
                x - mark, y, x + mark, y, fill=COLOR_LAST_MOVE_MARK, width=2,
            )
            self.canvas.create_line(
                x, y - mark, x, y + mark, fill=COLOR_LAST_MOVE_MARK, width=2,
            )
    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------
    def on_click(self, event):
        '''Handle a left click: translate it to a move and redraw.'''
        move = self.pixel_to_board(event.x, event.y)
        if move is None:
            return
        row, col = move
        if self.game.make_move(row, col):
            self.refresh()
    def refresh(self):
        '''Redraw the board and update the status message.'''
        self.draw_board()
        self.status_label.config(text=self.game.get_status_message())
    def restart(self):
        '''Reset the game and refresh the whole interface.'''
        self.game.reset()
        self.refresh()
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        '''Start the tkinter event loop.'''
        self.root.mainloop()