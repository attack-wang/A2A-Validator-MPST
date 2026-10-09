def partition(free, words_by_len):
    # words_by_len: dict len -> list of available words (we'll consume)
    free = set(free)
    result = []
    def neighbors(c):
        x, y = c
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==0 and dy==0: continue
                n = (x+dx, y+dy)
                if n in free: yield n
    def build_path(start, length):
        # random self-avoiding path of exact `length` starting at start, within free
        path = [start]
        used = {start}
        def dfs(cur):
            if len(path) == length: return True
            nbrs = [n for n in neighbors(cur) if n not in used]
            random.shuffle(nbrs)
            # heuristic: prefer cells with fewer free neighbors to avoid isolation? 
            for n in nbrs:
                # check viability: after removing path cells, does every free cell still have potential? skip complex check
                used.add(n); path.append(n)
                if dfs(n): return True
                path.pop(); used.remove(n)
            return False
        if dfs(start): return path
        return None