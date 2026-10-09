class StrandsGame:
    def __init__(self, puzzle=None):
        self.puzzle = puzzle
        self.found_words = []      # list of found target words (normalized)
        self.selection = []        # ordered list of selected strand ids
        self._consumed_ids = set()
        self.last_result = None
    def load_puzzle(self, puzzle): ...
    def select_strand(self, strand_id) -> bool:
        # reject if no puzzle, strand missing, consumed, already selected
        # append to selection
    def deselect_strand(self, strand_id): ...
    def clear_selection(self): ...
    def attempt_merge(self) -> MergeResult:
        # empty selection guard
        # word = normalize(concat of selected texts in selection order)
        # check unfound targets
        # check already found targets
        # check COMMON_WORDS
        # else invalid
    def get_hint(self):
        # pick first unfound target; find_segmentations over available strands; return first strand id of first segmentation or None
    def is_complete(self): ...
    def progress(self): ...