'''
player.py
Human player interaction for Mastermind.
Reads guesses from the terminal, validates them against the active
palette and code length, and turns single-letter shortcuts such as
"RGBY" into a full guess of color names. Also handles difficulty
selection and yes/no prompts.
'''
from colors import active_colors, build_letter_map, letter_for
from config import DEFAULT_DIFFICULTY, DIFFICULTIES
class Player:
    """Collects and validates the human player's input."""
    def __init__(self, color_names):
        self.color_names = color_names
        self.letter_map = build_letter_map(color_names)
    def _resolve_token(self, token):
        """Resolve one input token (letter or full name) to a color name."""
        lowered = token.lower()
        if lowered in self.letter_map:
            return self.letter_map[lowered]
        for name in self.color_names:
            if name.lower() == lowered:
                return name
        return None
    def get_guess(self, code_length, attempt, max_attempts):
        """Prompt until the player enters a valid guess; return color names."""
        prompt = (
            f"\nAttempt {attempt}/{max_attempts} - enter your guess of "
            f"{code_length} colors "
            f"({''.join(letter_for(c).lower() for c in self.color_names)}): "
        )
        while True:
            raw = input(prompt).strip()
            if not raw:
                print("  Empty input - please enter a guess.")
                continue
            tokens = raw.replace(",", " ").split()
            if len(tokens) != code_length:
                print(f"  Expected {code_length} colors, got {len(tokens)}. Try again.")
                continue
            resolved = [self._resolve_token(token) for token in tokens]
            if any(color is None for color in resolved):
                unknown = [t for t, c in zip(tokens, resolved) if c is None]
                print(f"  Unknown color(s): {', '.join(unknown)}. "
                      f"Valid letters: {''.join(sorted(self.letter_map))}. Try again.")
                continue
            return resolved
    @staticmethod
    def choose_difficulty():
        """Show the difficulty menu and return GameEngine kwargs."""
        print("\nSelect a difficulty:")
        keys = sorted(DIFFICULTIES)
        for key in keys:
            spec = DIFFICULTIES[key]
            print(f"  [{key}] {spec['name']:<6} - code length {spec['code_length']}, "
                  f"{spec['palette_size']} colors, {spec['max_attempts']} attempts")
        while True:
            choice = input(f"Choose 1-{keys[-1]} (default: {DEFAULT_DIFFICULTY}): ").strip()
            if not choice:
                choice = DEFAULT_DIFFICULTY
            if choice in DIFFICULTIES:
                spec = DIFFICULTIES[choice]
                return {
                    "code_length": spec["code_length"],
                    "palette_size": spec["palette_size"],
                    "max_attempts": spec["max_attempts"],
                }
            print("  Invalid choice - please enter a listed number.")