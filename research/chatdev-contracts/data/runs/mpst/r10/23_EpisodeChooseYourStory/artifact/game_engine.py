'''
Game engine for "The Whispering Vale" interactive storytelling game.
Drives the main menu, the narrative play loop, conditional choice
filtering, effect application, branching resolution, endings, and
in-game save support.
'''
from conditions import check_conditions
from effects import apply_effects
from save_load import STORY, save_game, load_game
from story_state import GameState
class GameEngine:
    """Runs the interactive story: menus, nodes, choices, and endings."""
    def __init__(self, story=None):
        self.story = story if story is not None else STORY
        self.state = None
    # -- title & menu ---------------------------------------------------
    def _print_title(self):
        print("=" * 60)
        print("        T H E   W H I S P E R I N G   V A L E")
        print("      An interactive tale of choices and consequences")
        print("=" * 60)
    def run(self):
        self._print_title()
        while True:
            choice = self._main_menu()
            if choice == "1":
                self.state = GameState(current_node="start")
                self._play()
            elif choice == "2":
                self._load_and_play()
            elif choice == "3":
                print("Farewell, traveler. The Vale keeps its whispers.")
                break
            else:
                print("Please enter 1, 2, or 3.")
    def _main_menu(self):
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        return input("> ").strip()
    def _load_and_play(self):
        try:
            self.state = load_game()
        except FileNotFoundError:
            print("No saved game found.")
            return
        except (ValueError, KeyError, TypeError):
            print("Save file is corrupted...")
            return
        if self.state.current_node not in self.story:
            print("Save points to unknown node; starting fresh.")
            self.state = GameState(current_node="start")
        self._play()
    # -- core play loop --------------------------------------------------
    def _play(self):
        while True:
            node = self.story.get(self.state.current_node)
            if node is None:
                self._show_ending({"ending": "The Wanderer's Road"})
                return
            self._show_node(node)
            if "ending" in node:
                self._show_ending(node)
                return
            choices = self._available_choices(node)
            if not choices:
                print("The path fades... The Wanderer's Road awaits.")
                self._show_ending({"ending": "The Wanderer's Road"})
                return
            for i, ch in enumerate(choices, 1):
                print(f"  {i}. {ch['text']}")
            print("\nCommands: (s)ave  (q)uit to menu  or enter a choice number")
            raw = input("> ").strip().lower()
            if raw in ("s", "save"):
                self._save()
                continue
            if raw in ("q", "quit", "menu"):
                print("Returning to the main menu...")
                return
            if not raw.isdigit() or not (1 <= int(raw) <= len(choices)):
                print("Enter a choice number, 's' to save, or 'q' to quit.")
                continue
            chosen = choices[int(raw) - 1]
            apply_effects(self.state, chosen.get("effects"))
            self.state.record(self.state.current_node, chosen["text"])
            next_node = self._resolve_next(chosen)
            if next_node is None or next_node not in self.story:
                print("The path fades... The Wanderer's Road awaits.")
                self._show_ending({"ending": "The Wanderer's Road"})
                return
            self.state.current_node = next_node
    # -- helpers (restored / merged fragments) ---------------------------
    def _show_node(self, node):
        print("\n" + "=" * 60)
        print(node["text"])
    def _available_choices(self, node):
        """Return only the choices whose conditions pass for current state."""
        return [
            ch for ch in node.get("choices", [])
            if check_conditions(self.state, ch.get("conditions"))
        ]
    def _resolve_next(self, choice):
        """Resolve a choice's 'next': a node id, or a conditional branch list."""
        next_spec = choice.get("next")
        if isinstance(next_spec, str):
            return next_spec
        if isinstance(next_spec, list):
            for branch in next_spec:
                if check_conditions(self.state, branch.get("conditions")):
                    return branch.get("next")
        return None
    def _show_ending(self, node):
        print("\n" + "*" * 60)
        print(f"           ENDING: {node['ending']}")
        print("*" * 60)
        print("Your journey through the Vale concludes here.")
        print(f"Choices made : {len(self.state.history)}")
        print(f"Items carried: {', '.join(self.state.items) if self.state.items else 'none'}")
        print(f"Variables    : {self.state.variables}")
        print("Thank you for playing!")
    def _save(self):
        try:
            path = save_game(self.state)
            print(f"Game saved to '{path}'.")
        except OSError as exc:
            print(f"Could not save: {exc}")