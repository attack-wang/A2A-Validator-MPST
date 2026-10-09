'''puzzle.py — data model for a Strands puzzle.'''
class Puzzle:
    def __init__(self, theme, description, strands, targets, key_target=None):
        self.theme = theme
        self.description = description
        self.strands = [s.upper() for s in strands]
        self.targets = [t.upper() for t in targets]
        self.key_target = key_target.upper() if key_target else None
        # sanity checks
        if self.key_target and self.key_target not in self.targets: raise ValueError
        # verify every target can be formed by concatenating strands? That's a nice integrity check.
    @staticmethod
    def normalize(text): return ''.join(text.split()).upper()
    def can_form(self, target): check via recursive segmentation using strands multiset
    def total_strand_letters vs target letters check