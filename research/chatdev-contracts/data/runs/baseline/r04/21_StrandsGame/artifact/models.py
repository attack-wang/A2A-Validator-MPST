class Puzzle:
    def __init__(self, title, theme_hint, targets: List[TargetWord], seed=None):
        self.title = title
        self.theme_hint = theme_hint
        self.targets = targets
        self.strands: List[Strand] = []
        self._build_strands(seed)
    def _build_strands(self, seed):
        rng = random.Random(seed)
        pieces = []
        sid = 0
        for t in self.targets:
            for s in t.strand_texts:
                pieces.append(Strand(sid, s.upper(), t.word))
                sid += 1
        rng.shuffle(pieces)
        # reassign display order? keep strand_id as identity, shuffle list order for display
        self.strands = pieces
    def strand_by_id(self, sid): ...
    @property
    def total_strands(self): ...