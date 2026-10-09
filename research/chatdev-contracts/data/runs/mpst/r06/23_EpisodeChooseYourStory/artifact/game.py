class Scene:
    def __init__(self, scene_id, title, text, choices=None, on_enter_effects=None,
                 is_ending=False, ending_name=None, conditional_text=None):
        self.scene_id = scene_id
        self.title = title
        self.text = list(text) if text else []
        self.choices = list(choices) if choices else []
        self.on_enter_effects = build_effects(on_enter_effects)
        self.is_ending = bool(is_ending)
        self.ending_name = ending_name
        self.conditional_text = [...]  # list of {"conditions": [...], "text": "..."}