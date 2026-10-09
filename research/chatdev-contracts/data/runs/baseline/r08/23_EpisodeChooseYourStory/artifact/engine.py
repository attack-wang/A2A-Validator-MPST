'''
engine.py
The game loop for the interactive storytelling game.
Presents narrative nodes, resolves conditional 'auto' transitions, applies
choice effects to GameState, detects endings, and handles save/quit.
'''
from game_state import GameState
from condition_evaluator import ConditionEvaluator
from ui import UI
class GameEngine:
    """Drives the story: node presentation, branching, effects, endings."""
    def __init__(self, story, state=None):
        self.story = story
        self.state = state if state is not None else GameState()
    # --- effects ---
    def apply_effects(self, effects):
        """Apply a choice's 'effects' dict to the game state."""
        if not effects:
            return
        for name, delta in effects.get("relationships", {}).items():
            self.state.modify_relationship(name, delta)
        for item in effects.get("add_items", []):
            self.state.add_item(item)
        for item in effects.get("remove_items", []):
            self.state.remove_item(item)
        for name, value in effects.get("flags", {}).items():
            self.state.set_flag(name, value)
        for name, delta in effects.get("variables", {}).items():
            self.state.adjust_variable(name, delta)
        for name, value in effects.get("set_variables", {}).items():
            self.state.set_variable(name, value)
    # --- conditional branching ---
    def resolve_auto(self, node_id):
        """
        Follow 'auto' conditional transitions until a presentable node is
        reached. Returns (node_id, node). Guards against cycles.
        """
        seen = set()
        node = self.story[node_id]
        while "auto" in node:
            if node_id in seen:
                raise ValueError(f"Auto-transition cycle detected at '{node_id}'.")
            seen.add(node_id)
            for branch in node["auto"]:
                if ConditionEvaluator.evaluate(branch.get("conditions", []), self.state):
                    node_id = branch["next"]
                    node = self.story[node_id]
                    break
            else:
                raise KeyError(
                    f"Node '{node_id}' has 'auto' transitions with no fallback branch."
                )
        return node_id, node
    # --- player input ---
    def get_player_choice(self, choices):
        """Prompt until a valid choice number, 's' (status) or 'q' (quit)."""
        options = [c["text"] for c in choices]
        while True:
            UI.show_choices(options)
            raw = input("> ").strip().lower()
            if raw in ("s", "status"):
                UI.print_wrapped(self.state.summary())
                continue
            if raw in ("q", "quit"):
                confirm = input("Save and quit? (y/n) > ").strip().lower()
                if confirm in ("y", "yes"):
                    return None
                continue
            if raw.isdigit():
                index = int(raw)
                if 1 <= index <= len(choices):
                    return choices[index - 1]
            UI.print_wrapped(
                f"Enter a number 1-{len(choices)}, 's' for status, or 'q' to save & quit."
            )
    def show_status(self):
        """Print the current state summary."""
        UI.print_wrapped(self.state.summary())
    # --- main loop ---
    def run(self):
        """Run the story from the current node until an ending or quit."""
        node_id = self.state.current_node
        while True:
            node_id, node = self.resolve_auto(node_id)
            self.state.current_node = node_id
            if node_id not in self.state.history:
                self.state.history.append(node_id)
            UI.clear()
            UI.title(node.get("title", "Untitled"))
            UI.type_out(node["text"])
            if node.get("ending"):
                UI.separator()
                UI.print_wrapped("*** THE END ***")
                UI.separator()
                UI.print_wrapped("Thanks for playing. (Saved progress cleared.)")
                self.state.clear_save()
                return
            choice = self.get_player_choice(node["choices"])
            if choice is None:
                self.state.save()
                UI.print_wrapped("Progress saved. Goodbye!")
                return
            self.apply_effects(choice.get("effects"))
            self.state.choices_made.append([node_id, choice["text"]])
            node_id = choice["next"]