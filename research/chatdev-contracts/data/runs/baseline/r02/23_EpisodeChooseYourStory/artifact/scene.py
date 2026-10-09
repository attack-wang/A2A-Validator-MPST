@dataclass Choice: text, next, effects=None, conditions=None, hint=None
@dataclass Ending: name, epilogue (maybe inside scene)
@dataclass Scene: id, title, text (raw), choices, on_enter=None, ending=None
def load_scenes(raw: dict) -> dict[str, Scene]