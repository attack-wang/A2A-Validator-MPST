def generate(words, spangram, rows=6, cols=8, attempts=...):
    for attempt in range(N):
        grid = empty
        placements = []
        # try to place spangram: random path from one side to opposite side
        # then place other words randomly
        if backtrack_fill(...): return grid, placements