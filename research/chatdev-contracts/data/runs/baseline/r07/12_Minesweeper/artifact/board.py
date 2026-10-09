if len(candidates) < self.total_mines:
    candidates = [cell for cell in all_cells if not cell.has_mine()]
    # protect only clicked cell
    candidates = [c for c in all_cells if c is not self.cells[safe_row][safe_col]]