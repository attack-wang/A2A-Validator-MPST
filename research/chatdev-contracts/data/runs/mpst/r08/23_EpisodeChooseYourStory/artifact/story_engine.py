'''
story_engine.py
StoryEngine: the core game loop. Walks the story graph node by node,
applies on-enter effects (guarded against loop re-application), composes
narrative text with conditional variants, partitions choices into
available/locked via the ConditionEvaluator, applies chosen effects via the
EffectApplier, and routes to endings — with explicit fallback handling for
dead ends so the loop never returns None mid-game.
'''
from game_state import GameState
from conditions import ConditionEvaluator, ConditionError
from effects import EffectApplier, EffectError
from story_nodes import StoryNode, Choice
class StoryEngine:
    """Drives traversal of the story graph and player interaction."""
    def __init__(self, story, ui, state=None, evaluator=None, applier=None,
                 fallback_node_id=None):
        """Store the story dict, UI, state and helper components."""
        self.story = story                      # node_id -> StoryNode
        self.ui = ui
        self.state = state if state is not None else GameState()
        self.evaluator = evaluator if evaluator is not None else ConditionEvaluator()
        self.applier = applier if applier is not None else EffectApplier()
        self.fallback_node_id = fallback_node_id  # safe route for dead ends
    def compose_text(self, node):
        """Base node text plus any variant text whose condition passes."""
        parts = [node.text]
        for variant in node.variants:
            try:
                if self.evaluator.evaluate(variant["condition"], self.state):
                    parts.append(variant["text"])
            except ConditionError:
                # Malformed variant conditions should not crash the game;
                # skip the variant but keep the base narrative intact.
                continue
        return "\n\n".join(parts)
    def run(self, start_node_id):
        """Main game loop: present nodes, gather choices, route to endings."""
        node_id = start_node_id
        while True:
            node = self.story.get(node_id)
            if node is None:
                # Broken target reference: use fallback or synthesize an ending.
                node_id = self._handle_missing_node(node_id)
                continue
            # Apply on-enter effects only on first visit so loops don't re-fire.
            first_visit = node_id not in self.state.history
            if first_visit:
                self.applier.apply_all(node.on_enter, self.state)
            self.state.record_visit(node_id)
            text = self.compose_text(node)
            if node.is_ending:
                self.state.record_ending(node_id)
                self.ui.show_ending(node, text)
                return node
            self.ui.show_narrative(text)
            # Partition choices into available and locked (with hints).
            available, locked = [], []
            for choice in node.choices:
                if choice.is_available(self.state, self.evaluator):
                    available.append(choice)
                else:
                    locked.append(choice)
            if not available:
                # Dead end: no legal choice remains — route to fallback.
                node_id = self._handle_dead_end(node)
                continue
            self.ui.show_choices(available, locked)
            idx = self.ui.get_choice(len(available))
            choice = available[idx]
            self.state.record_choice(node_id, choice.text)
            self.applier.apply_all(choice.effects, self.state)
            self.ui.show_effects_feedback(choice.effects, self.applier)
            node_id = choice.target
    def _handle_missing_node(self, bad_id):
        """Resolve a dangling target reference without crashing."""
        if self.fallback_node_id and self.fallback_node_id in self.story:
            self.ui.show_system_message(
                f"[Story warning: '{bad_id}' is missing; rerouting to fallback.]")
            return self.fallback_node_id
        # No fallback defined: synthesize a graceful ending.
        self.ui.show_system_message(
            f"[Story warning: '{bad_id}' is missing; ending the run safely.]")
        end_id = "__missing_node_ending__"
        self.story[end_id] = StoryNode(
            end_id,
            "The path ahead dissolves into mist. Your story ends here — "
            "for now.",
            is_ending=True,
            ending_name="Lost in the Mist",
            ending_tone="neutral",
        )
        return end_id
    def _handle_dead_end(self, node):
        """Resolve a node whose choices are all locked or absent."""
        if self.fallback_node_id and self.fallback_node_id in self.story:
            self.ui.show_system_message(
                "[No choices are available here; the story reroutes...]")
            return self.fallback_node_id
        # Without a fallback, close the run with a synthesized ending.
        end_id = f"__dead_end_ending__{node.node_id}"
        self.story[end_id] = StoryNode(
            end_id,
            "Every path from here is closed to you. Your journey ends "
            "where the roads run out.",
            is_ending=True,
            ending_name="A Closed Road",
            ending_tone="somber",
        )
        return end_id