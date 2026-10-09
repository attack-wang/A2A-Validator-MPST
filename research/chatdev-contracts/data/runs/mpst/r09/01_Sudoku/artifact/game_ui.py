'''
game_ui.py
Defines the GameUI class, a Tkinter-based graphical interface for the
Sudoku game. It renders the 9x9 grid on a canvas, handles mouse and
keyboard input for selecting and filling cells, displays mistake
highlights, and shows the completion dialog when the puzzle is solved.
'''
import tkinter as tk
from tkinter import ttk, messagebox
class GameUI:
    """Tkinter graphical interface for the Sudoku game."""
    CELL_SIZE = 56
    MARGIN = 20
    BOARD_PX = CELL_SIZE * 9  # 504
    BG_COLOR = "#ffffff"
    GIVEN_BG = "#e8e8e8"
    SELECT_BG = "#fff3b0"
    CONFLICT_BG = "#ff9d9d"
    GIVEN_FG = "#333333"
    USER_FG = "#1565c0"
    CONFLICT_FG = "#b00020"
    LINE_COLOR = "#333333"
    BOX_LINE_COLOR = "#000000"
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.root.resizable(False, False)
        top = tk.Frame(self.root)
        top.pack(fill=tk.X, padx=self.MARGIN, pady=(8, 0))
        tk.Label(top, text="Sudoku", font=("Arial", 18, "bold")).pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self.root,
                                width=self.BOARD_PX + 2 * self.MARGIN,
                                height=self.BOARD_PX + 2 * self.MARGIN,
                                bg=self.BG_COLOR, highlightthickness=0)
        self.canvas.pack(padx=self.MARGIN, pady=8)
        self.status = tk.Label(self.root, text="", anchor="w",
                               font=("Arial", 11), fg="#444444")
        self.status.pack(fill=tk.X, padx=self.MARGIN)
        controls = tk.Frame(self.root)
        controls.pack(fill=tk.X, padx=self.MARGIN, pady=(4, 10))
        tk.Label(controls, text="Difficulty:").pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="Medium")
        ttk.Combobox(controls, textvariable=self.difficulty_var,
                     values=["Easy", "Medium", "Hard"],
                     state="readonly", width=8).pack(side=tk.LEFT, padx=(4, 10))
        tk.Button(controls, text="New Game",
                  command=self._on_new_game).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="Check Mistakes",
                  command=self.controller.check_mistakes).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="Hint",
                  command=self.controller.give_hint).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="Clear Cell",
                  command=self.controller.clear_selected).pack(side=tk.LEFT, padx=4)
        self.canvas.bind("<Button-1>", self._on_click)
        self.root.bind("<Key>", self._on_key)
        self.canvas.focus_set()
    def _on_new_game(self):
        """Start a new game at the difficulty chosen in the dropdown."""
        self.controller.new_game(self.difficulty_var.get())
    def _on_click(self, event):
        """Translate a left-click into a cell selection on the board."""
        col = (event.x - self.MARGIN) // self.CELL_SIZE
        row = (event.y - self.MARGIN) // self.CELL_SIZE
        if 0 <= row < 9 and 0 <= col < 9:
            self.controller.select_cell(int(row), int(col))
    def _on_key(self, event):
        """Handle arrow keys, digits, and clear keys."""
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if event.keysym in moves:
            self.controller.move_selection(*moves[event.keysym])
        elif event.keysym in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            self.controller.enter_value(int(event.keysym))
        elif event.keysym in ("BackSpace", "Delete", "0"):
            self.controller.clear_selected()
    def render(self, board, selected, conflicts, message=""):
        """Draw grid, thick 3x3 box lines, cell coloring, and digits."""
        self.canvas.delete("all")
        o = self.MARGIN
        for r in range(9):
            for c in range(9):
                x1 = o + c * self.CELL_SIZE
                y1 = o + r * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                if (r, c) in conflicts:
                    bg, fg = self.CONFLICT_BG, self.CONFLICT_FG
                elif selected == (r, c):
                    bg, fg = self.SELECT_BG, self.USER_FG
                elif board.is_given(r, c):
                    bg, fg = self.GIVEN_BG, self.GIVEN_FG
                else:
                    bg, fg = self.BG_COLOR, self.USER_FG
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=bg, outline=self.LINE_COLOR)
                value = board.get_value(r, c)
                if value:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                            text=str(value),
                                            font=("Arial", 20, "bold"), fill=fg)
        # thin inner lines are drawn by cell outlines; draw thick box lines
        for i in range(0, 10, 3):
            self.canvas.create_line(o + i * self.CELL_SIZE, o,
                                    o + i * self.CELL_SIZE, o + self.BOARD_PX,
                                    fill=self.BOX_LINE_COLOR, width=3)
            self.canvas.create_line(o, o + i * self.CELL_SIZE,
                                    o + self.BOARD_PX, o + i * self.CELL_SIZE,
                                    fill=self.BOX_LINE_COLOR, width=3)
        # outer border
        self.canvas.create_rectangle(o, o, o + self.BOARD_PX, o + self.BOARD_PX,
                                     outline=self.BOX_LINE_COLOR, width=3)
        if message:
            self.status.config(text=message)
    def show_status(self, message):
        """Display a transient status message under the board."""
        self.status.config(text=message)
    def show_completion(self):
        """Show a dialog congratulating the player on solving the puzzle."""
        messagebox.showinfo("Puzzle Solved",
                            "Congratulations! You completed the Sudoku puzzle correctly.")
    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()