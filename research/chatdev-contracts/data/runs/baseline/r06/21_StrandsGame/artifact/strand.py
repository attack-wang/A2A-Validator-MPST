'''
strand.py — Strand data model for the Strands word-segmentation puzzle.
'''
class Strand:
    def __init__(self, sid, text):
        self.sid = sid
        self.text = text.upper()
        self.merged_into = None
    @property
    def is_available(self):
        return self.merged_into is None
    def assign(self, word):
        self.merged_into = word
    def release(self):
        self.merged_into = None
    def __repr__(self):
        return f"Strand({self.sid}, '{self.text}')"
    def __str__(self):
        status = f"→ {self.merged_into}" if self.merged_into else "available"
        return f"[{self.sid}] {self.text} ({status})"