'''
gui.py
Tkinter front-end for the Reversi (Othello) game.
Draws the 8x8 board on a Canvas, highlights valid moves, animates disc
placement and flips, shows live scores, handles pass messages and the
final game-over dialog.
'''
import tkinter as tk
from tkinter import messagebox
from board import BLACK, WHITE, EMPTY, BOARD_SIZE
from game import GameController
# --- Layout / appearance constants -------------------------------------
CELL_SIZE = 62
MARGIN = 16
BOARD_PIXELS = CELL_SIZE * BOARD_SIZE
CANVAS_SIZE = BOARD_PIXELS + MARGIN * 2
BOARD_COLOR = "#0b7a3e"   # classic green felt
LINE_COLOR = "#04522a"
HINT_COLOR = "#a8e6b0"    # light dots for valid moves
LAST_MOVE_COLOR = "#ffd54a"
DISC_COLORS = {BLACK: "#161616", WHITE: "#f5f5f5"}
DISC_EDGE = {BLACK: "#000000", WHITE: "#9a9a9a"}
# --- Fonts --------------------------------------------------------------
NORMAL_FONT = ("Helvetica", 13, "bold")
ACTIVE_FONT = ("Helvetica", 13, "bold", "underline")
STATUS_FONT = ("Helvetica", 12)
COORD_FONT = ("Helvetica", 9)
# --- Animation constants -------------------------------------------------
ANIM_STEPS = 8
ANIM_DELAY_MS = 35
class ReversiGUI:
    '''Interactive Tkinter view + input layer for the Reversi game.'''
    def __init__(self, root):
        '''Build all widgets, initialise animation state and draw the board.'''
        self.root = root
        self.controller = GameController()
        self.animating = False
        self._anim = None          # data dict for the running animation
        self._anim_job = None      # id of the scheduled after() callback
        self._message_job = None   # id of the scheduled message clear
        self._game_over_shown = False
        self._build_widgets()
        self.refresh()
    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------
    def _build_widgets(self):
        '''Create the header, canvas, status label and control buttons.'''
        self.root.title("Reversi (Othello)")
        self.root.resizable(False, False)
        header = tk.Frame(self.root)
        header.pack(pady=(8, 2))
        self.black_score_frame, self.black_score_label = self._make_score_widget(header, BLACK)
        self.black_score_frame.pack(side="left", padx=14)
        self.white_score_frame, self.white_score_label = self._make_score_widget(header, WHITE)
        self.white_score_frame.pack(side="left", padx=14)
        self.message_label = tk.Label(self.root, text="", font=STATUS_FONT, fg="#b23c00")
        self.message_label.pack(pady=(0, 4))
        self.canvas = tk.Canvas(self.root, width=CANVAS_SIZE, height=CANVAS_SIZE,
                                bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.pack(padx=10, pady=4)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        controls = tk.Frame(self.root)
        controls.pack(pady=(2, 10))
        self.new_game_button = tk.Button(controls, text="New Game", command=self.new_game, width=12)
        self.new_game_button.pack()
    def _make_score_widget(self, parent, color):
        '''Build a score display: a coloured disc dot next to a text label.
        Returns (frame, label) so the caller can keep a reference to the label.
        '''
        frame = tk.Frame(parent)
        dot = tk.Canvas(frame, width=18, height=18, highlightthickness=0)
        dot.create_oval(2, 2, 16, 16, fill=DISC_COLORS[color], outline=DISC_EDGE[color])
        dot.pack(side="left")
        label = tk.Label(frame, text="", font=NORMAL_FONT)
        label.pack(side="left", padx=(4, 0))
        return frame, label
    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def _cell_center(self, row, col):
        '''Return the (x, y) pixel coordinates of a cell's centre.'''
        x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        return x, y
    def _draw_board(self):
        '''Draw the grid lines and coordinate labels on the canvas.'''
        for i in range(BOARD_SIZE + 1):
            # horizontal lines
            self.canvas.create_line(MARGIN, MARGIN + i * CELL_SIZE,
                                    MARGIN + BOARD_PIXELS, MARGIN + i * CELL_SIZE,
                                    fill=LINE_COLOR)
            # vertical lines
            self.canvas.create_line(MARGIN + i * CELL_SIZE, MARGIN,
                                    MARGIN + i * CELL_SIZE, MARGIN + BOARD_PIXELS,
                                    fill=LINE_COLOR)
        self._draw_coordinates()
    def _draw_coordinates(self):
        '''Draw column letters (a-h) on top and row numbers (1-8) on the left.'''
        letters = "abcdefgh"
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE + CELL_SIZE // 2
            # letters on top
            self.canvas.create_text(x, MARGIN - 8, text=letters[i],
                                    fill="#e8f5e9", font=COORD_FONT)
            # numbers on left
            y = MARGIN + i * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(MARGIN - 8, y, text=str(i + 1),
                                    fill="#e8f5e9", font=COORD_FONT)
    def _draw_disc(self, row, col, player, radius=None):
        '''Draw a single disc centred in the given cell.'''
        x, y = self._cell_center(row, col)
        if radius is None:
            radius = CELL_SIZE // 2 - 4
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=DISC_COLORS[player], outline=DISC_EDGE[player], width=1)
    def _draw_hints(self):
        '''Draw small dots on every cell where the current player may move.'''
        for r, c in self.controller.board.get_valid_moves(self.controller.current_player):
            x, y = self._cell_center(r, c)
            radius = 5
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                    fill=HINT_COLOR, outline="")
    def _draw_last_move_marker(self):
        '''Outline the cell of the most recently placed disc.'''
        if self.controller.last_move:
            r, c = self.controller.last_move
            x, y = self._cell_center(r, c)
            radius = CELL_SIZE // 2 - 4
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                    outline=LAST_MOVE_COLOR, width=2)
    # ------------------------------------------------------------------
    # Refresh / scores / status
    # ------------------------------------------------------------------
    def refresh(self):
        '''Redraw the whole board and update scores, turn text and game-over dialog.'''
        self.canvas.delete("all")
        self._draw_board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                disc = self.controller.board.get_disc(r, c)
                if disc != EMPTY:
                    self._draw_disc(r, c, disc)
        if not self.controller.game_over and not self.animating:
            self._draw_hints()
        self._draw_last_move_marker()
        self.update_scores()
        self._update_status()
        if self.controller.game_over and not self._game_over_shown:
            self._game_over_shown = True
            self._show_game_over_dialog()
    def update_scores(self):
        '''Refresh the score labels and highlight whose turn it is.'''
        black, white = self.controller.get_scores()
        self.black_score_label.config(text=f"Black: {black}")
        self.white_score_label.config(text=f"White: {white}")
        if self.controller.game_over:
            self.black_score_label.config(font=NORMAL_FONT)
            self.white_score_label.config(font=NORMAL_FONT)
        else:
            active = self.controller.current_player
            self.black_score_label.config(font=ACTIVE_FONT if active == BLACK else NORMAL_FONT)
            self.white_score_label.config(font=ACTIVE_FONT if active == WHITE else NORMAL_FONT)
    def _update_status(self):
        '''Set the status text describing the current turn or a pass event.'''
        if self.controller.game_over:
            self.message_label.config(text="Game over — press New Game to play again.")
            return
        player_name = "Black" if self.controller.current_player == BLACK else "White"
        text = f"{player_name}'s turn"
        if self.controller.skipped_player:
            skipped_name = "Black" if self.controller.skipped_player == BLACK else "White"
            text += f"  ({skipped_name} has no valid move and passes)"
        self.message_label.config(text=text, fg="#204d00")
    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def flash_message(self, text, duration=2200):
        '''Show a temporary warning message that clears itself after duration ms.'''
        self.message_label.config(text=text, fg="#b23c00")
        if self._message_job:
            self.root.after_cancel(self._message_job)
        self._message_job = self.root.after(duration, self.clear_message)
    def clear_message(self):
        '''Erase the temporary message and cancel any pending clear job.'''
        if self._message_job:
            self.root.after_cancel(self._message_job)
            self._message_job = None
        self.message_label.config(text="")
        # restore normal turn text
        if not self.controller.game_over:
            self._update_status()
    # ------------------------------------------------------------------
    # Input handling
    # ------------------------------------------------------------------
    def on_canvas_click(self, event):
        '''Translate a canvas click into a board move and trigger the animation.'''
        if self.animating or self.controller.game_over:
            return
        col = (event.x - MARGIN) // CELL_SIZE
        row = (event.y - MARGIN) // CELL_SIZE
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        player = self.controller.current_player
        flipped = self.controller.make_move(row, col)
        if flipped is None:
            self.flash_message("Invalid move — choose a highlighted cell.")
            return
        self.update_scores()
        self.start_animation((row, col), flipped, player)
    # ------------------------------------------------------------------
    # Animation
    # ------------------------------------------------------------------
    def start_animation(self, placed, flipped, player):
        '''Begin animating the newly placed disc and all flipped discs.'''
        self.animating = True
        self._anim = {
            "step": 0,
            "placed": placed,
            "flipped": flipped,
            "player": player,
        }
        self._anim_job = self.root.after(ANIM_DELAY_MS, self._animate)
    def _animate(self):
        '''Advance the flip animation one step; refresh the board when done.'''
        if not self._anim:
            self.animating = False
            self._anim_job = None
            return
        self._anim["step"] += 1
        step = self._anim["step"]
        player = self._anim["player"]
        # Redraw the static board, then overlay the animated discs.
        self.canvas.delete("all")
        self._draw_board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                disc = self.controller.board.get_disc(r, c)
                if disc != EMPTY:
                    self._draw_disc(r, c, disc)
        # The placed disc grows from small to full size.
        pr, pc = self._anim["placed"]
        grow = step / ANIM_STEPS
        radius = int((CELL_SIZE // 2 - 4) * (0.3 + 0.7 * grow))
        self._draw_disc(pr, pc, player, radius=radius)
        # Flipped discs shrink then regrow in the new colour.
        for r, c in self._anim["flipped"]:
            if step <= ANIM_STEPS // 2:
                # shrinking in old colour
                old = WHITE if player == BLACK else BLACK
                radius = int((CELL_SIZE // 2 - 4) * (1 - 0.8 * (step / (ANIM_STEPS // 2))))
                self._draw_disc(r, c, old, radius=max(radius, 4))
            else:
                # growing in new colour
                t = (step - ANIM_STEPS // 2) / (ANIM_STEPS - ANIM_STEPS // 2)
                radius = int((CELL_SIZE // 2 - 4) * (0.2 + 0.8 * t))
                self._draw_disc(r, c, player, radius=radius)
        if step >= ANIM_STEPS:
            self.animating = False
            self._anim = None
            self._anim_job = None
            self.refresh()
        else:
            self._anim_job = self.root.after(ANIM_DELAY_MS, self._animate)
    # ------------------------------------------------------------------
    # Game-over dialog / new game
    # ------------------------------------------------------------------
    def _show_game_over_dialog(self):
        '''Display a dialog with the final score and the winner (or a tie).'''
        black, white = self.controller.get_scores()
        if self.controller.winner == BLACK:
            result = "Black wins!"
        elif self.controller.winner == WHITE:
            result = "White wins!"
        else:
            result = "It's a tie!"
        messagebox.showinfo("Game Over", f"Final score — Black: {black}  White: {white}\n\n{result}")
    def new_game(self):
        '''Reset the game state, cancel any running animation and redraw.'''
        if self._anim_job:
            self.root.after_cancel(self._anim_job)
            self._anim_job = None
        if self._message_job:
            self.root.after_cancel(self._message_job)
            self._message_job = None
        self.controller.reset()
        self.animating = False
        self._anim = None
        self._game_over_shown = False
        self.refresh()