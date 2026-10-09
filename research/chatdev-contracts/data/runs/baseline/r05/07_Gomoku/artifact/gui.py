'''
GUI module: renders the Gomoku board with tkinter and handles user interaction.
'''
import tkinter as tk
from tkinter import messagebox
from config import (BOARD_SIZE, CELL_SIZE, MARGIN, STONE_RADIUS,
                    BOARD_WIDTH, BOARD_HEIGHT,
                    COLOR_BACKGROUND, COLOR_LINE, COLOR_STAR,
                    COLOR_BLACK_STONE, COLOR_WHITE_STONE,
                    COLOR_HIGHLIGHT, COLOR_STATUS_BG, COLOR_STATUS_FG,
                    BLACK, WHITE)
from game import GameState
class GomokuGUI:
    '''Tkinter-based graphical interface for the Gomoku game.'''
    def __init__(self, game):
        '''Build the main window, board canvas and status bar, then draw the empty board.'''
        self.game = game
        self.root = tk.Tk()
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        # Board canvas
        self.canvas = tk.Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT,
                                bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        # Status bar
        self.status_label = tk.Label(self.root, text=self.game.get_state_message(),
                                     font=("Arial", 14), bg=COLOR_STATUS_BG,
                                     fg=COLOR_STATUS_FG, width=40, pady=8)
        self.status_label.pack(fill=tk.X)
        # Restart button
        self.restart_button = tk.Button(self.root, text="Restart Game",
                                        font=("Arial", 12), command=self.restart)
        self.restart_button.pack(pady=6)
        self.draw_board()
    def draw_board(self):
        '''Draw the wooden background, grid lines and star points.'''
        # Outer border
        pad = 4
        self.canvas.create_rectangle(MARGIN - pad, MARGIN - pad,
                                     BOARD_WIDTH - MARGIN + pad, BOARD_HEIGHT - MARGIN + pad,
                                     outline=COLOR_LINE, width=2)
        # Grid lines
        for i in range(BOARD_SIZE):
            pos = MARGIN + i * CELL_SIZE
            self.canvas.create_line(MARGIN, pos, BOARD_WIDTH - MARGIN, pos,
                                    fill=COLOR_LINE, width=1)
            self.canvas.create_line(pos, MARGIN, pos, BOARD_HEIGHT - MARGIN,
                                    fill=COLOR_LINE, width=1)
        # Star points (standard hoshi points on a 15x15 board)
        for r, c in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            self.draw_star_point(r, c)
    def draw_star_point(self, row, col):
        '''Draw a small dot marking a star (hoshi) point.'''
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        radius = 4
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=COLOR_STAR, outline=COLOR_STAR)
    def draw_stone(self, row, col, player):
        '''Draw a black or white stone centered on the intersection (row, col).'''
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        color = COLOR_BLACK_STONE if player == BLACK else COLOR_WHITE_STONE
        outline = COLOR_BLACK_STONE if player == BLACK else "#888888"
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS,
                                fill=color, outline=outline, width=1)
    def on_canvas_click(self, event):
        '''Translate a mouse click into a board move and refresh the display.'''
        if self.game.state != GameState.ONGOING:
            return
        col = round((event.x - MARGIN) / CELL_SIZE)
        row = round((event.y - MARGIN) / CELL_SIZE)
        # Ignore clicks far from any intersection
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        nearest_x = MARGIN + col * CELL_SIZE
        nearest_y = MARGIN + row * CELL_SIZE
        if abs(event.x - nearest_x) > CELL_SIZE / 2 or abs(event.y - nearest_y) > CELL_SIZE / 2:
            return
        player = self.game.current_player
        if not self.game.handle_move(row, col):
            return  # Invalid move (occupied intersection)
        self.draw_stone(row, col, player)
        self.refresh()
    def refresh(self):
        '''Update the status bar and react to a finished game.'''
        self.status_label.config(text=self.game.get_state_message())
        if self.game.state in (GameState.BLACK_WINS, GameState.WHITE_WINS):
            self.highlight_winning_line()
            winner = self.game.get_state_message()
            self.root.after(100, lambda: messagebox.showinfo("Game Over", winner))
        elif self.game.state == GameState.DRAW:
            self.root.after(100, lambda: messagebox.showinfo("Game Over", self.game.get_state_message()))
    def highlight_winning_line(self):
        '''Draw red rings around the stones that form the winning line.'''
        for row, col in self.game.winning_line:
            x = MARGIN + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE
            self.canvas.create_oval(x - STONE_RADIUS - 3, y - STONE_RADIUS - 3,
                                    x + STONE_RADIUS + 3, y + STONE_RADIUS + 3,
                                    outline=COLOR_HIGHLIGHT, width=2)
    def restart(self):
        '''Reset the game and redraw a clean board.'''
        self.game.restart()
        self.canvas.delete("all")
        self.draw_board()
        self.status_label.config(text=self.game.get_state_message())
    def run(self):
        '''Start the tkinter main loop.'''
        self.root.mainloop()