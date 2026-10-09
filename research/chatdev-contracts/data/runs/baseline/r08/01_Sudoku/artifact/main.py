    def _place_digit(self, value):
        """Put a digit into the selected cell, report conflicts and check completion."""
        if self.selected is None or self.game_over:
            return
        row, col = self.selected
        if not self.board.is_editable(row, col):
            self._set_status("That cell is a fixed clue and cannot be changed.")
            return
        self.board.set_value(row, col, value)
        self.hinted.discard((row, col))
        self._draw_board()
        if (row, col) in self.board.find_conflicts():
            self._set_status(f"Mistake: {value} conflicts with its row, column or 3x3 box.")
        else:
            self._set_status(f"Placed {value} at row {row + 1}, column {col + 1}.")
        if self.board.is_complete():
            self._victory()
    def _erase_selected(self):
        """Clear the selected editable cell."""
        if self.selected is None or self.game_over:
            return
        row, col = self.selected
        if self.board.clear_value(row, col):
            self.hinted.discard((row, col))
            self._set_status(f"Cleared row {row + 1}, column {col + 1}.")
            self._draw_board()
        else:
            self._set_status("That cell is a fixed clue and cannot be erased.")
    def _on_erase(self):
        """Erase button handler."""
        self._erase_selected()
    # ------------------------------------------------------- check / hint
    def _on_check(self):
        """Check the current board for mistakes and report progress."""
        if self.game_over:
            return
        conflicts = self.board.find_conflicts()
        if conflicts:
            cells = ", ".join(f"R{r + 1}C{c + 1}" for r, c in sorted(conflicts))
            self._set_status(f"Mistakes found in {len(conflicts)} cell(s): {cells}")
        elif self.board.is_full():
            self._victory()
        else:
            remaining = len(self.board.get_empty_cells())
            self._set_status(f"No mistakes so far! {remaining} cell(s) left to fill.")
        self._draw_board()
    def _on_hint(self):
        """Fill the selected cell with the correct solution value."""
        if self.game_over:
            return
        if self.selected is None:
            self._set_status("Select a cell first to get a hint.")
            return
        row, col = self.selected
        if self.board.is_fixed(row, col):
            self._set_status("That cell already holds a correct clue.")
            return
        value = self.board.get_hint(row, col)
        if value is None:
            self._set_status("No hint available for this puzzle.")
            return
        self.board.set_value(row, col, value)
        self.hinted.add((row, col))
        self._draw_board()
        self._set_status(f"Hint: {value} placed at row {row + 1}, column {col + 1}.")
        if self.board.is_complete():
            self._victory()
    # ---------------------------------------------------------- rendering
    def _draw_board(self):
        """Render the grid, cell backgrounds, digits and thick box lines."""
        self.canvas.delete("all")
        conflicts = self.board.find_conflicts()
        # Cells holding the same digit as the selected cell get highlighted.
        same_cells = set()
        if self.selected is not None:
            value = self.board.get_value(*self.selected)
            if value != self.board.EMPTY:
                for r in range(self.board.SIZE):
                    for c in range(self.board.SIZE):
                        if self.board.get_value(r, c) == value:
                            same_cells.add((r, c))
        for r in range(self.board.SIZE):
            for c in range(self.board.SIZE):
                x0 = self.MARGIN + c * self.CELL_SIZE
                y0 = self.MARGIN + r * self.CELL_SIZE
                x1, y1 = x0 + self.CELL_SIZE, y0 + self.CELL_SIZE
                value = self.board.get_value(r, c)
                if (r, c) == self.selected:
                    bg = self.SELECTED_BG
                elif (r, c) in conflicts:
                    bg = self.CONFLICT_BG
                elif (r, c) in same_cells:
                    bg = self.SAME_BG
                elif (r, c) in self.hinted:
                    bg = self.HINT_BG
                elif self.board.is_fixed(r, c):
                    bg = self.FIXED_BG
                else:
                    bg = self.USER_BG
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="")
                if value != self.board.EMPTY:
                    color = self.CONFLICT_FG if (r, c) in conflicts else (
                        self.FIXED_FG if self.board.is_fixed(r, c) else self.USER_FG)
                    weight = "bold" if self.board.is_fixed(r, c) else "normal"
                    self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2,
                                            text=str(value), fill=color,
                                            font=("Helvetica", 20, weight))
        # Grid lines: thin lines between cells, thick lines around 3x3 boxes.
        for i in range(10):
            if i % 3 == 0:
                color, width = self.BOX_LINE, 3
            else:
                color, width = self.GRID_LINE, 1
            x = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(x, self.MARGIN, x, self.MARGIN + 9 * self.CELL_SIZE,
                                    fill=color, width=width)
            y = self.MARGIN + i * self.CELL_SIZE
            self.canvas.create_line(self.MARGIN, y, self.MARGIN + 9 * self.CELL_SIZE, y,
                                    fill=color, width=width)
    # ---------------------------------------------------------- completion
    def _victory(self):
        """Confirm completion: stop the timer, celebrate and invite a new game."""
        self.game_over = True
        self.timer_running = False
        if self._timer_job is not None:
            self.root.after_cancel(self._timer_job)
            self._timer_job = None
        minutes, seconds = divmod(self.elapsed, 60)
        self._set_status(f"Puzzle solved in {minutes}m {seconds}s. Congratulations!")
        self._draw_board()
        messagebox.showinfo("Sudoku", f"Congratulations! You solved the puzzle in {minutes}m {seconds}s.\n\nStart a new game whenever you like.")
def main():
    """Create the root window, launch the GUI and start the main loop."""
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()