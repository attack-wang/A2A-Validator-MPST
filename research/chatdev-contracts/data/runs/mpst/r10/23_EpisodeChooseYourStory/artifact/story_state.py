class GameState:
    def __init__(self, variables=None, items=None, flags=None, history=None, current_node=None):
        self.variables = dict(variables or {})
        self.items = list(items or [])
        self.flags = set(flags or [])
        self.history = list(history or [])
        self.current_node = current_node
    def get_variable(self, name, default=0):
        return self.variables.get(name, default)
    def change_variable(self, name, delta):
        self.variables[name] = self.variables.get(name, 0) + delta
        return self.variables[name]
    def set_variable(self, name, value):
        self.variables[name] = value
        return value
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    def has_item(self, item):
        return item in self.items
    def set_flag(self, flag):
        self.flags.add(flag)
    def clear_flag(self, flag):
        self.flags.discard(flag)
    def has_flag(self, flag):
        return flag in self.flags
    def record(self, node_id, choice_text):
        self.history.append((node_id, choice_text))
    def to_dict(self):
        return {
            "variables": dict(self.variables),
            "items": list(self.items),
            "flags": sorted(self.flags),  # set -> list for JSON
            "history": [list(entry) for entry in self.history],
            "current_node": self.current_node,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            variables=data.get("variables", {}),
            items=data.get("items", []),
            flags=set(data.get("flags", [])),
            history=[tuple(entry) for entry in data.get("history", [])],
            current_node=data.get("current_node"),
        )