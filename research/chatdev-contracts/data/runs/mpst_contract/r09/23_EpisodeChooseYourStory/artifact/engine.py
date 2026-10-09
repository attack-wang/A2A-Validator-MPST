"""Game engine: state tracking, conditional checks, and the story loop."""
import textwrap


class GameState:
    """Tracks variables, items, and the path taken through the story."""

    def __init__(self):
        self.vars = {"trust": 0, "courage": 0, "companion": 0}
        self.items = set()
        self.path = []


class GameEngine:
    def __init__(self, story, start):
        self.story = story
        self.state = GameState()
        self.current = start

    # --- condition DSL --------------------------------------------------
    def _check(self, cond):
        """True if cond holds. cond may be None, a dict, or a list (AND)."""
        if not cond:
            return True
        if isinstance(cond, list):
            return all(self._check(c) for c in cond)
        if "item" in cond and cond["item"] not in self.state.items:
            return False
        for k, v in cond.get("min", {}).items():
            if self.state.vars.get(k, 0) < v:
                return False
        for k, v in cond.get("max", {}).items():
            if self.state.vars.get(k, 0) > v:
                return False
        for k, v in cond.get("eq", {}).items():
            if self.state.vars.get(k) != v:
                return False
        return True

    def _apply(self, effects):
        if not effects:
            return
        for item in effects.get("gain", []):
            self.state.items.add(item)
        for item in effects.get("lose", []):
            self.state.items.discard(item)
        for k, d in effects.get("add", {}).items():
            self.state.vars[k] = self.state.vars.get(k, 0) + d
        for k, v in effects.get("set", {}).items():
            self.state.vars[k] = v

    # --- presentation -----------------------------------------------------
    @staticmethod
    def _wrap(text):
        return "\n".join(textwrap.wrap(text, width=70))

    def _prompt(self, choices):
        for i, c in enumerate(choices, 1):
            print(f"  {i}. {c['label']}")
        while True:
            raw = input("> ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(choices):
                return choices[int(raw) - 1]
            print(f"  Choose 1-{len(choices)}.")

    def run(self):
        print("=" * 70)
        print("T H E   H O L L O W   C R O W N".center(70))
        print("an interactive tale".center(70))
        print("=" * 70)
        while self.current:
            node = self.story[self.current]
            self.state.path.append(self.current)
            print()
            print(self._wrap(node["text"]))
            if node.get("ending"):
                self._finish()
                return
            choices = [c for c in node["choices"] if self._check(c.get("if"))]
            if not choices:
                print("\nThe tale ends here, unresolved.")
                return
            print()
            choice = self._prompt(choices)
            self._apply(choice.get("effects"))
            self.current = choice["next"]

    def _finish(self):
        print("\n" + "-" * 70)
        print("JOURNEY'S END".center(70))
        print("-" * 70)
        print(f"Items carried : {', '.join(sorted(self.state.items)) or 'none'}")
        rels = ", ".join(f"{k}={v}" for k, v in sorted(self.state.vars.items()))
        print(f"Relationships : {rels}")
        print(f"Path taken    : {' -> '.join(self.state.path)}")
        print("\nThanks for playing!")