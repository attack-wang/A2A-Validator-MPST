'''
effects.py
EffectApplier: mutates a GameState according to declarative effect
dictionaries attached to choices or node entries. Supported: add_item,
remove_item, set_flag, clear_flag, adjust_relationship, set_relationship,
set_variable, adjust_variable.
'''
class EffectError(Exception):
    """Raised when an effect dictionary has an unknown or invalid type."""
class EffectApplier:
    """Applies declarative effect dicts to a GameState."""
    def __init__(self):
        # Dispatch table mapping effect type -> handler method.
        self._handlers = {
            "add_item": self._add_item,
            "remove_item": self._remove_item,
            "set_flag": self._set_flag,
            "clear_flag": self._clear_flag,
            "adjust_relationship": self._adjust_relationship,
            "set_relationship": self._set_relationship,
            "set_variable": self._set_variable,
            "adjust_variable": self._adjust_variable,
        }
    def apply(self, effect, state):
        """Apply a single effect dict to the state.
        Raises EffectError for unknown types so typos in story data fail fast.
        """
        if not isinstance(effect, dict) or "type" not in effect:
            raise EffectError(f"Malformed effect (missing 'type'): {effect!r}")
        etype = effect["type"]
        handler = self._handlers.get(etype)
        if handler is None:
            raise EffectError(f"Unknown effect type: {etype!r}")
        handler(effect, state)
    def apply_all(self, effects, state):
        """Apply a list of effects in order; empty/None lists are no-ops."""
        for effect in (effects or []):
            self.apply(effect, state)
    # ----- primitive handlers -----
    def _add_item(self, effect, state):
        """Add an item to the player's inventory."""
        state.add_item(effect["item"])
    def _remove_item(self, effect, state):
        """Remove an item from the player's inventory."""
        state.remove_item(effect["item"])
    def _set_flag(self, effect, state):
        """Record a one-shot event flag."""
        state.set_flag(effect["flag"])
    def _clear_flag(self, effect, state):
        """Clear a one-shot event flag."""
        state.clear_flag(effect["flag"])
    def _adjust_relationship(self, effect, state):
        """Shift a character's relationship score by delta."""
        state.adjust_relationship(effect["character"], effect["delta"])
    def _set_relationship(self, effect, state):
        """Overwrite a character's relationship score."""
        state.ensure_relationship(effect["character"])
        state.relationships[effect["character"]] = effect["value"]
    def _set_variable(self, effect, state):
        """Overwrite a named variable."""
        state.set_variable(effect["name"], effect["value"])
    def _adjust_variable(self, effect, state):
        """Shift a numeric variable by delta (defaults to 0 if unset)."""
        current = state.get_variable(effect["name"], 0)
        state.set_variable(effect["name"], current + effect["delta"])
    def describe(self, effect):
        """Return a short human-readable string, e.g. '+2 Mira trust'."""
        etype = effect.get("type", "?") if isinstance(effect, dict) else "?"
        descriptions = {
            "add_item": lambda e: f"+item {e.get('item', '?')}",
            "remove_item": lambda e: f"-item {e.get('item', '?')}",
            "set_flag": lambda e: f"flag: {e.get('flag', '?')}",
            "clear_flag": lambda e: f"clear flag: {e.get('flag', '?')}",
            "adjust_relationship": lambda e: f"{e.get('delta', 0):+d} {e.get('character', '?')} trust",
            "set_relationship": lambda e: f"{e.get('character', '?')} trust = {e.get('value', '?')}",
            "set_variable": lambda e: f"{e.get('name', '?')} = {e.get('value', '?')}",
            "adjust_variable": lambda e: f"{e.get('name', '?')} {e.get('delta', 0):+d}",
        }
        builder = descriptions.get(etype)
        return builder(effect) if builder else etype