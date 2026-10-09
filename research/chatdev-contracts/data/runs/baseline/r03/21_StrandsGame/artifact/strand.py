class Strand:
    """A single text fragment displayed on the board."""
    def __init__(self, sid, text):
        self.sid = sid      # two-character display id, e.g. "03"
        self.text = text    # fragment text, e.g. "TER"
        self.used = False   # True once consumed by a valid merge