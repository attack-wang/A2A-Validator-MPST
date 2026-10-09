from strand import Strand
from solvabilitychecker import SolvabilityChecker
class Puzzle:
    def __init__(self, title, theme, targets, strands, spangram=None, dictionary=None):
        self.title = title
        self.theme = theme
        self.targets = [t.upper() for t in targets]  # display forms
        self.spangram = spangram.upper() if spangram else None
        self.dictionary = dictionary or set()
        self.strands = [Strand(i + 1, text) for i, text in enumerate(strands)]
    @classmethod
    def from_definition(cls, definition, dictionary):
        puzzle = cls(
            title=definition["title"],
            theme=definition["theme"],
            targets=definition["targets"],
            strands=definition["strands"],
            spangram=definition.get("spangram"),
            dictionary=dictionary,
        )
        if not SolvabilityChecker.is_solvable(puzzle):
            # warn
            ...
        return puzzle