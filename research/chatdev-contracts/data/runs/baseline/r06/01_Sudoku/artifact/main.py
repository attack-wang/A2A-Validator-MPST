    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_top_bar(self):
        """Create the header with the title and difficulty selector."""
        header = tk.Frame(self.root, bg=self.BG_COLOR)
        header.pack(fill="x", padx=12, pady=(10, 0))
        tk.Label(
            header, text="SUDOKU", font=("Helvetica", 20, "bold"),
            bg=self.BG_COLOR, fg="#222222"
        ).pack(side="left")
        tk.Label(
            header, text="Difficulty:", font=("Helvetica", 11),
            bg=self.BG_COLOR, fg="#222222"
        ).pack(side="left", padx=(20, 4))
        difficulty_menu = ttk.Combobox(
            header, textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"], state="readonly", width=8
        )
        difficulty_menu.pack(side="left")
        difficulty_menu.bind("<<ComboboxSelected>>", self._on_difficulty_change)
    def _build_canvas(self):
        """Create the canvas on which the board is drawn."""
        size = self.BOARD_SIZE + 2 * self.MARGIN
        self.canvas = tk.Canvas(
            self.root, width=size, height=size,
            bg=self.BG_COLOR, highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=8)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
    def _build_controls(self):
        """Create the number pad, action buttons and status bar."""
        controls = tk.Frame(self.root, bg=self.BG_COLOR)
        controls.pack(fill="x", padx=12, pady=(0, 4))
        # Number pad 1-9
        pad = tk.Frame(controls, bg=self.BG_COLOR)
        pad.pack(side="left")
        for number in range(1, 10):
            tk.Button(
                pad, text=str(number), width=3, font=("Helvetica", 12, "bold"),
                command=lambda n=number: self.enter_number(n)
            ).grid(row=0, column=number - 1, padx=2)
        # Action buttons
        actions = tk.Frame(controls, bg=self.BG_COLOR)
        actions.pack(side="right")
        tk.Button(actions, text="Erase", width=7, command=self.erase_selection).grid(row=0, column=0, padx=2)
        tk.Button(actions, text="Check", width=7, command=self.check_mistakes).grid(row=0, column=1, padx=2)
        tk.Button(actions, text="Hint", width=7, command=self.reveal_hint).grid(row=0, column=2, padx=2)
        tk.Button(actions, text="New Game", width=9, command=self._on_new_game).grid(row=0, column=3, padx=2)
        # Mistake toggle + status bar
        bottom = tk.Frame(self.root, bg=self.BG_COLOR)
        bottom.pack(fill="x", padx=12, pady=(0, 10))
        tk.Checkbutton(
            bottom, text="Highlight mistakes", variable=self.show_mistakes_var,
            command=self.redraw, bg=self.BG_COLOR, font=("Helvetica", 10)
        ).pack(side="left")
        self.status_label = tk.Label(
            bottom, textvariable=self.status_var,
            bg=self.BG_COLOR, font=("Helvetica", 11, "bold"), fg=self.STATUS_OK
        )
        self.status_label.pack(side="right")
    def _bind_keys(self):
        """Bind keyboard shortcuts: digits, erase keys and arrow navigation."""
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Up>", lambda e: self.move_selection(-1, 0))
        self.root.bind("<Down>", lambda e: self.move_selection(1, 0))
        self.root.bind("<Left>", lambda e: self.move_selection(0, -1))
        self.root.bind("<Right>", lambda e: self.move_selection(0, 1))
    # ------------------------------------------------------------------
    # Game flow
    # ------------------------------------------------------------------
    def new_game(self, difficulty):
        """Generate a fresh puzzle and reset all game state."""
        self.difficulty = difficulty
        self.game_over = False
        self.mistake_count = 0
        self.selected = None
        puzzle, solution = self.generator.generate_puzzle(difficulty)
        self.solution = [row[:] for row in solution]
        self.board.reset(puzzle)
        self._set_status(f"New {difficulty} puzzle. Good luck!", ok=True)
        self.redraw()
    def on_canvas_click(self, event):
        """Select the cell under the mouse cursor."""
        if self.game_over:
            return
        col = int((event.x - self.MARGIN) // self.CELL_SIZE)  # int cast: float index would crash
        row = int((event.y - self.MARGIN) // self.CELL_SIZE)
        self.selected = (row, col) if self.board.in_bounds(row, col) else None
        self.redraw()
    def on_key_press(self, event):
        """Digits 1-9 enter a value; BackSpace/Delete/0 erase."""
        if self.game_over:
            return
        if event.char and event.char in "123456789":  # guard: "" is "in" any string!
            self.enter_number(int(event.char))
        elif event.keysym in ("BackSpace", "Delete") or event.char == "0":
            self.erase_selection()
    def move_selection(self, drow, dcol):
        """Move the selection with the arrow keys, clamped to the grid."""
        if self.game_over:
            return
        if self.selected is None:
            self.selected = (0, 0)
        else:
            row = min(max(self.selected[0] + drow, 0), self.board.SIZE - 1)
            col = min(max(self.selected[1] + dcol, 0), self.board.SIZE - 1)
            self.selected = (row, col)
        self.redraw()
    def enter_number(self, number):
        """Place a digit in the selected editable cell, then check completion."""
        if self.game_over or self.selected is None:
            return
        row, col = self.selected
        if self.board.is_fixed(row, col):
            self._set_status("Fixed clue — cannot be changed.", ok=False)
            return
        if self.board.set_value(row, col, number):
            if not self.board.is_valid_placement(row, col, number):
                self.mistake_count += 1
            self.redraw()
            self._check_completion()
    def erase_selection(self):
        """Clear the selected editable cell."""
        if self.game_over or self.selected is None:
            return
        if self.board.clear_value(*self.selected):
            self.redraw()
    def check_mistakes(self):
        """Report conflicts; highlight them in red via redraw()."""
        conflicts = self.board.find_conflicts()
        if conflicts:
            self._set_status(f"{len(conflicts)} conflicting cell(s) shown in red.", ok=False)
        else:
            self._set_status("No mistakes so far — keep going!", ok=True)
        self.redraw()
    def reveal_hint(self):
        """Fill the selected empty cell (or the first empty cell) from the solution."""
        if self.game_over:
            return
        target = self.selected if (self.selected and self.board.is_empty(*self.selected)) \
            else self.board.find_empty()
        if target:
            row, col = target
            self.board.set_value(row, col, self.solution[row][col])
            self.selected = target
            self.redraw()
            self._check_completion()
    def _check_completion(self):
        """Confirm completion: lock input and show the victory dialog."""
        if self.board.is_complete():
            self.game_over = True
            self._set_status("Puzzle solved — congratulations!", ok=True)
            self.redraw()
            messagebox.showinfo(
                "Sudoku",
                f"You solved the puzzle!\nMistakes made: {self.mistake_count}"
            )
    def _set_status(self, message, ok=True):
        """Update the status bar text and colour."""
        self.status_var.set(message)
        self.status_label.config(fg=self.STATUS_OK if ok else self.STATUS_ERROR)
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def redraw(self):
        """Repaint the board: conflicts, selection, peers, then grid lines."""
        self.canvas.delete("all")
        conflicts = self.board.find_conflicts() if self.show_mistakes_var.get() else set()
        sel = self.selected
        sel_val = self.board.get_value(*sel) if sel else None
        for row in range(self.board.SIZE):
            for col in range(self.board.SIZE):
                self._draw_cell(row, col, conflicts, sel, sel_val)
        self._draw_grid_lines()
        if sel is not None:
            self._draw_selection_border()
    def _draw_cell(self, row, col, conflicts, sel, sel_val):
        """Draw one cell; background priority: conflict > selected > same-number > peer > fixed."""
        x0 = self.MARGIN + col * self.CELL_SIZE
        y0 = self.MARGIN + row * self.CELL_SIZE
        x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE
        value = self.board.get_value(row, col)
        is_fixed = self.board.is_fixed(row, col)
        if (row, col) in conflicts:
            bg = self.CONFLICT_BG
        elif sel == (row, col):
            bg = self.SELECTED_BG
        elif sel_val and value == sel_val:
            bg = self.SAME_NUMBER_BG
        elif sel and (row == sel[0] or col == sel[1] or
                      (row // 3, col // 3) == (sel[0] // 3, sel[1] // 3)):
            bg = self.PEER_BG
        else:
            bg = self.FIXED_CELL_BG if is_fixed else self.USER_CELL_BG
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="")
        if value:
            self.canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2, text=str(value),
                font=("Helvetica", 22, "bold"),
                fill=self.FIXED_TEXT if is_fixed else self.USER_TEXT
            )
    def _draw_grid_lines(self):
        """Draw thin cell lines and thick 3x3 subgrid separators."""
        for i in range(10):
            thick = (i % 3 == 0)
            color = self.THICK_LINE_COLOR if thick else self.LINE_COLOR
            width = 3 if thick else 1
            p = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(p, self.MARGIN, p, self.MARGIN + self.BOARD_SIZE, fill=color, width=width)
            self.canvas.create_line(self.MARGIN, p, self.MARGIN + self.BOARD_SIZE, p, fill=color, width=width)
    def _draw_selection_border(self):
        """Draw a bold border around the selected cell."""
        row, col = self.selected
        x0 = self.MARGIN + col * self.CELL_SIZE
        y0 = self.MARGIN + row * self.CELL_SIZE
        self.canvas.create_rectangle(
            x0, y0, x0 + self.CELL_SIZE, y0 + self.CELL_SIZE,
            outline=self.THICK_LINE_COLOR, width=3
        )
    # ------------------------------------------------------------------
    # Menu callbacks
    # ------------------------------------------------------------------
    def _on_new_game(self):
        """Start a new game with the currently selected difficulty."""
        self.new_game(self.difficulty_var.get())
    def _on_difficulty_change(self, event):
        """Restart with a new puzzle whenever the difficulty changes."""
        self.new_game(self.difficulty_var.get())
def main():
    """Launch the Sudoku application."""
    root = tk.Tk()
    SudokuGUI(root, difficulty="medium")
    root.mainloop()
if __name__ == "__main__":
    main()