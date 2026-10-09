best = None
best_candidates = None
for r in range(self.SIZE):
    for c in range(self.SIZE):
        if board[r][c] == 0:
            candidates = [...]
            if best_candidates is None or len(candidates) < len(best_candidates):
                best = (r, c)
                best_candidates = candidates
                if len(candidates) <= 1:
                    break
    else:
        continue
    break