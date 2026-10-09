        for br in range(0, self.SIZE, self.BOX_SIZE):
            for bc in range(0, self.SIZE, self.BOX_SIZE):
                seen = {}
                for r in range(br, br + self.BOX_SIZE):
                    for c in range(bc, bc + self.BOX_SIZE):
                        v = self.grid[r][c]
                        if v == self.EMPTY:
                            continue
                        if v in seen:
                            conflicts.add(seen[v])
                            conflicts.add((r, c))
                        else:
                            seen[v] = (r, c)