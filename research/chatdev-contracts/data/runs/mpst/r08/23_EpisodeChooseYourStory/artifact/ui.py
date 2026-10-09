'''
ui.py
ConsoleUI: a console-based user interface for the interactive story.
Renders narrative text, numbered choice lists (locked choices shown with
their unlock hints), ending screens, a live status panel of tracked
variables (inventory, relationships, flags), and effect feedback. All
player input passes through a validation loop.
'''
class ConsoleUI:
    """Console rendering and validated input for the story engine."""
    WIDTH = 70  # wrap width for horizontal rules
    # ----- rendering helpers -----
    def _rule(self, char="-"):
        """Return a horizontal rule line."""
        return char * self.WIDTH
    def _wrap(self, text):
        """Soft-wrap text to WIDTH columns using textwrap."""
        import textwrap
        lines = []
        for paragraph in text.split("\n"):
            lines.extend(textwrap.wrap(paragraph, self.WIDTH) or [""])
        return "\n".join(lines)
    def show_narrative(self, text):
        """Print a narrative segment inside a framed block."""
        print()
        print(self._rule())
        print(self._wrap(text))
        print(self._rule())
    def show_status(self, state):
        """Display tracked variables: inventory, relationships, flags."""
        print()
        print("[ Status ]")
        if state.inventory:
            print(f"  Inventory: {', '.join(state.inventory)}")
        else:
            print("  Inventory: (empty)")
        if state.relationships:
            rels = ", ".join(f"{name}: {score:+d}"
                             for name, score in sorted(state.relationships.items()))
            print(f"  Relationships: {rels}")
        else:
            print("  Relationships: (none yet)")
        if state.flags:
            print(f"  Flags: {', '.join(sorted(state.flags))}")
        print()
    def show_choices(self, available, locked):
        """Print numbered available choices, then locked ones with hints."""
        print("\nWhat will you do?")
        for i, choice in enumerate(available, start=1):
            print(f"  {i}. {choice.text}")
        if locked:
            print("  ---")
            print("  (Locked options — how they might open:)")
            for choice in locked:
                print(f"  [locked] {choice.text} — {choice.describe_locked(None, None)}")
        print()
    def get_choice(self, n):
        """Prompt until the player enters a valid number 1..n."""
        while True:
            raw = input("> ").strip()
            if raw.isdigit() and 1 <= int(raw) <= n:
                return int(raw) - 1
            print(f"Please enter a number between 1 and {n}.")
    def show_ending(self, node, text):
        """Print an ending screen with name and tone."""
        print()
        print("=" * self.WIDTH)
        print(f"*** ENDING: {node.ending_name or 'The End'} "
              f"({node.ending_tone}) ***")
        print("=" * self.WIDTH)
        print(self._wrap(text))
        print("=" * self.WIDTH)
        print()
    def show_effects_feedback(self, effects, applier):
        """Print short descriptions of the effects just applied."""
        if not effects:
            return
        parts = [applier.describe(e) for e in effects]
        print(f"  >> {', '.join(parts)}")
    def show_system_message(self, message):
        """Print an engine/system notice."""
        print(f"  {message}")
    def show_goodbye(self, state):
        """Print a closing summary of the run."""
        print("Thanks for playing!")
        print(f"  Nodes visited: {len(set(state.history))}")
        print(f"  Choices made: {len(state.choices_made)}")
        print(f"  Endings discovered: {len(state.endings_discovered)}")