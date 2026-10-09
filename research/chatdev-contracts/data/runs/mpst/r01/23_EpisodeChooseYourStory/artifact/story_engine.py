'''
story_engine.py
Core engine for the interactive storytelling game "The Hollow Shrine".
Responsibilities:
    - Store the story as a structured graph (dict: node_id -> StoryNode).
    - Present narrative segments and condition-gated choices.
    - Apply choice effects to the GameState (items, flags, relationships,
      variables).
    - Route the player to the next node and detect endings.
    - Guard against broken links and dead ends so the game can never
      crash or soft-lock mid-story.
Classes:
    Choice      - one selectable option, gated by an optional condition,
                  carrying effects and the id of the next story node.
    StoryNode   - one narrative segment with text, choices, optional
                  on-enter effects, and optional ending information.
    StoryEngine - walks the story graph, evaluates conditions against the
                  GameState, applies effects, and runs the interactive loop.
Also provides build_default_story(), which constructs the structured
story graph used by the game and demonstrates every required feature:
branching choices, conditional gating, state-mutating effects, and six
distinct endings shaped by the player's accumulated state.
'''
import textwrap
from conditions import evaluate_condition
from game_state import GameState
class Choice:
    """A single selectable option inside a story node."""
    def __init__(self, text, next_node, condition=None, effects=None):
        """
        Create a choice.
        Args:
            text: str shown to the player.
            next_node: id of the node to move to when this choice is taken.
            condition: optional condition dict gating availability
                       (None means always available).
            effects: optional list of effect dicts applied when taken.
        """
        self.text = text
        self.next_node = next_node
        self.condition = condition
        self.effects = effects
    def is_available(self, game_state):
        """Return True when the choice's condition passes (None = always)."""
        return evaluate_condition(self.condition, game_state)
class StoryNode:
    """One narrative segment of the story graph."""
    def __init__(self, node_id, text, choices=None, is_ending=False,
                 ending_name=None, on_enter=None):
        """
        Create a story node.
        Args:
            node_id: unique identifier used by choices to link here.
            text: narrative paragraph displayed when the node is entered.
            choices: list of Choice objects (empty for endings).
            is_ending: True if reaching this node finishes the story.
            ending_name: display name of the ending (endings only).
            on_enter: optional list of effect dicts applied once when
                      the player first enters this node.
        """
        self.node_id = node_id
        self.text = text
        self.choices = choices if choices is not None else []
        self.is_ending = is_ending
        self.ending_name = ending_name
        self.on_enter = on_enter
class StoryEngine:
    """Drives the interactive loop over a structured story graph."""
    def __init__(self, story, game_state, start_node="arrival"):
        """Store the graph, the player's state, and the starting node id."""
        self.story = story
        self.game_state = game_state
        self.current_node_id = start_node
    # ------------------------------------------------------------------
    # Graph utilities
    # ------------------------------------------------------------------
    def current_node(self):
        """Return the StoryNode the player is currently in.
        Raises:
            KeyError: if the current node id is missing from the graph
                      (a broken choice link).
        """
        node = self.story.get(self.current_node_id)
        if node is None:
            raise KeyError(
                f"Story graph has no node '{self.current_node_id}' "
                f"(broken choice link)"
            )
        return node
    def available_choices(self):
        """Return only the choices whose conditions pass right now."""
        return [choice for choice in self.current_node().choices
                if choice.is_available(self.game_state)]
    def validate_story(self):
        """Check every choice link points at an existing node.
        Returns:
            list: human-readable problems (empty if the graph is sound).
                  Called once before the game starts.
        """
        problems = []
        for node_id, node in self.story.items():
            if not node.choices and not node.is_ending:
                problems.append(
                    f"Node '{node_id}' has no choices and is not an "
                    f"ending (dead end)"
                )
            for choice in node.choices:
                if choice.next_node not in self.story:
                    problems.append(
                        f"Node '{node_id}' links to unknown node "
                        f"'{choice.next_node}'"
                    )
        return problems
    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------
    def advance(self, choice):
        """Record the choice, apply its effects, and enter the next node."""
        self.game_state.record_choice(self.current_node_id, choice.text)
        self.game_state.apply_effects(choice.effects)
        self._enter_node(choice.next_node)
    def _enter_node(self, node_id):
        """Move to a node, applying its one-time on_enter effects."""
        self.current_node_id = node_id
        node = self.current_node()
        if node_id not in self.game_state.visited_nodes:
            self.game_state.record_visit(node_id)
            self.game_state.apply_effects(node.on_enter)
    # ------------------------------------------------------------------
    # Presentation helpers
    # ------------------------------------------------------------------
    def _print_wrapped(self, text, width=78):
        """Print text wrapped to a readable console width."""
        for line in textwrap.wrap(text, width=width):
            print(line)
    def _show_ending(self, node):
        """Print the ending text plus a summary of the player's journey."""
        print("\n" + "=" * 78)
        print(f"ENDING: {node.ending_name or 'The End'}")
        print("=" * 78)
        self._print_wrapped(node.text)
        print("\n--- Your journey ---")
        print("Choices made:")
        for visited_id, choice_text in self.game_state.choice_history:
            print(f"  - [{visited_id}] {choice_text}")
        items = sorted(self.game_state.items)
        print(f"Items: {', '.join(items) if items else 'none'}")
        print("Relationships:")
        for who, level in sorted(self.game_state.relationships.items()):
            print(f"  - {who}: {level}")
        flags = sorted(self.game_state.flags)
        print(f"Flags: {', '.join(flags) if flags else 'none'}")
        print("\nThank you for playing.")
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the interactive game loop until an ending (or quit) is reached."""
        self._enter_node(self.current_node_id)
        print("\nThe Hollow Shrine - an interactive story")
        print("Type the number of a choice and press Enter. "
              "Type 'q' to quit.")
        while True:
            node = self.current_node()
            # Ending nodes terminate the story.
            if node.is_ending:
                self._show_ending(node)
                return
            # Present the narrative segment.
            print("\n" + "-" * 78)
            self._print_wrapped(node.text)
            print()
            # Present only the choices currently allowed by conditions.
            choices = self.available_choices()
            if not choices:
                # Dead-end guard: never soft-lock the player.
                self._print_wrapped(
                    "The path ahead is closed to you, and the story "
                    "ends here."
                )
                return
            for index, choice in enumerate(choices, start=1):
                print(f"  {index}. {choice.text}")
            try:
                raw = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nYou slip away from the story... until next time.")
                return
            if raw.lower() in ("q", "quit", "exit"):
                print("\nYou slip away from the story... until next time.")
                return
            try:
                index = int(raw)
            except ValueError:
                print("Please enter the number of a choice (or 'q' to quit).")
                continue
            if not 1 <= index <= len(choices):
                print(f"Please choose a number between 1 and {len(choices)}.")
                continue
            self.advance(choices[index - 1])
def build_default_story():
    """
    Build and return the structured story graph for 'The Hollow Shrine'.
    The graph demonstrates every required feature:
        - branching choices (most nodes offer several exits),
        - conditional gating (choices hidden unless items, flags,
          relationships, or variables allow),
        - effects that mutate state (items gained and spent, flags set,
          relationships changed, variables incremented),
        - six distinct endings shaped by the player's accumulated state.
    """
    nodes = {}
    def add(node):
        """Register a StoryNode in the graph and return it."""
        nodes[node.node_id] = node
        return node
    # --- opening -------------------------------------------------------
    add(StoryNode(
        "arrival",
        "Dusk settles over the village of Ashenbrook. Candles flicker in "
        "every window, and the air smells of woodsmoke and fear. A "
        "one-eyed scout named Ryse intercepts you on the road. 'Another "
        "traveler? Then you have heard - the Hollow Shrine has woken, and "
        "something inside it cries out every night.'",
        choices=[
            Choice(
                "Ask Ryse what she knows about the shrine.",
                "ryse_talk",
                effects=[{"type": "change_relationship",
                          "character": "ryse", "delta": 1}],
            ),
            Choice(
                "Thank her and head to the inn to question the locals.",
                "inn",
            ),
            Choice(
                "Push past her and go straight to the council hall.",
                "council",
            ),
        ],
    ))
    add(StoryNode(
        "ryse_talk",
        "Ryse lowers her voice. 'Twenty years ago the shrine's keeper died "
        "and no one took her place. Whatever sings in there now is not a "
        "monster - it is mourning. The council will not hear it; they only "
        "want the noise to stop.' She grips your shoulder. 'Choose your "
        "allies carefully, traveler.'",
        choices=[
            Choice("Visit the inn to hear the elder's side.", "inn"),
            Choice("Go to the council hall.", "council"),
            Choice("Search the old well by the shrine path before dark.",
                   "well"),
        ],
        on_enter=[
            {"type": "set_flag", "flag": "knows_truth"},
            {"type": "change_relationship", "character": "ryse", "delta": 1},
        ],
    ))
    add(StoryNode(
        "well",
        "The old well is dry and choked with ivy. Lowered on the last "
        "rope you find a small silver amulet shaped like a crescent moon "
        "- the old keeper's token, lost for twenty years. It hums "
        "faintly, as if remembering a song.",
        choices=[
            Choice("Pocket the amulet and head to the inn.", "inn"),
            Choice("Pocket the amulet and go to the council.", "council"),
        ],
        on_enter=[{"type": "add_item", "item": "moonlit_amulet"}],
    ))
    add(StoryNode(
        "inn",
        "The inn is warm and loud until you mention the shrine. An old "
        "woman by the fire waves you over. 'I was the keeper's friend,' "
        "she says. 'The spirit is the keeper's daughter, lost in the "
        "snow the night the shrine went dark. Sing her the lullaby her "
        "mother sang, and she will rest. But no one has dared.' She "
        "teaches you the melody, note by note.",
        choices=[
            Choice("Thank the elder and go to the council.", "council"),
            Choice("Slip out at once and head for the shrine.", "shrine_path"),
        ],
        on_enter=[
            {"type": "set_flag", "flag": "knows_truth"},
            {"type": "set_flag", "flag": "peaceful_intent"},
            {"type": "change_relationship", "character": "elder", "delta": 1},
        ],
    ))
    add(StoryNode(
        "council",
        "In the council hall, maps and torches crowd the walls. "
        "'Traveler!' the headman calls. 'Good - you look capable. At "
        "dawn we march to burn the Hollow Shrine and whatever whines "
        "inside it. Will you stand with us?'",
        choices=[
            Choice(
                "'I will confront the spirit - my way.' Volunteer.",
                "council_prep",
                effects=[
                    {"type": "increment_variable", "name": "courage",
                     "amount": 1},
                    {"type": "change_relationship", "character": "ryse",
                     "delta": 1},
                ],
            ),
            Choice(
                "'Burning it will only make it worse.' Slip away toward "
                "the shrine.",
                "shrine_path",
            ),
            Choice(
                "'This is not my fight.' Leave the village tonight.",
                "leave_village",
            ),
        ],
    ))
    add(StoryNode(
        "council_prep",
        "The armorer gives you a hooded lantern and a whetstone. Ryse "
        "watches you test the blade's weight. 'If you go up there "
        "tonight,' she says quietly, 'you will not go alone in spirit. "
        "Whatever you decide to do up there, decide it kindly.'",
        choices=[
            Choice("March for the shrine while the night is young.",
                   "shrine_path"),
        ],
        on_enter=[
            {"type": "add_item", "item": "lantern"},
            {"type": "increment_variable", "name": "courage", "amount": 1},
        ],
    ))
    add(StoryNode(
        "shrine_path",
        "The shrine rises out of the mist, its black door sealed with "
        "chains of shadow. A cold light pulses behind the stone. "
        "Whatever waits inside has waited twenty years.",
        choices=[
            Choice(
                "Raise the Moonlit Amulet to the black door.",
                "inner_sanctum",
                condition={"type": "has_item", "item": "moonlit_amulet"},
                effects=[
                    {"type": "remove_item", "item": "moonlit_amulet"},
                    {"type": "set_flag", "flag": "shrine_lit"},
                ],
            ),
            Choice(
                "Set your shoulder against the black door and push.",
                "inner_sanctum",
                condition={
                    "type": "or",
                    "conditions": [
                        {"type": "variable_at_least", "name": "courage",
                         "value": 1},
                        {"type": "relationship_at_least", "character": "ryse",
                         "value": 1},
                    ],
                },
                effects=[{"type": "set_flag", "flag": "door_forced"}],
            ),
            Choice(
                "This place is wrong. Turn back down the mountain.",
                "abandoned_quest",
            ),
        ],
    ))
    add(StoryNode(
        "inner_sanctum",
        "The sanctum is a circle of cold candles. In the center hovers a "
        "figure of silver mist - the keeper's daughter, singing a broken "
        "half-song to herself. When she sees you, the mist sharpens into "
        "something very like hope, or very like hunger.",
        choices=[
            Choice(
                "Sing the lullaby the elder taught you.",
                "peaceful_dawn",
                condition={
                    "type": "and",
                    "conditions": [
                        {"type": "flag_set", "flag": "peaceful_intent"},
                        {"type": "or", "conditions": [
                            {"type": "flag_set", "flag": "knows_truth"},
                            {"type": "has_item", "item": "moonlit_amulet"},
                        ]},
                    ],
                },
            ),
            Choice(
                "Hold out the Moonlit Amulet - her mother's token.",
                "token_gift",
                condition={"type": "has_item", "item": "moonlit_amulet"},
                effects=[{"type": "remove_item", "item": "moonlit_amulet"}],
            ),
            Choice(
                "Draw your blade and strike while she is formless.",
                "hollow_victory",
                condition={
                    "type": "or",
                    "conditions": [
                        {"type": "variable_at_least", "name": "courage",
                         "value": 2},
                        {"type": "relationship_at_least", "character": "ryse",
                         "value": 2},
                    ],
                },
            ),
            Choice(
                "Back away into the dark and run.",
                "fled_shrine",
            ),
        ],
    ))
    # --- endings ---------------------------------------------------------
    add(StoryNode(
        "peaceful_dawn",
        "Your voice finds the old melody in the cold air. The mist "
        "stills... then the spirit hums along, note by note, until the "
        "half-song is whole. As the first light of dawn touches the "
        "shrine, she bows to you and dissolves into silver fireflies. "
        "The Hollow Shrine is hollow no longer - it is only a shrine, "
        "and it is finally at rest.",
        is_ending=True,
        ending_name="The Lullaby's End",
    ))
    add(StoryNode(
        "token_gift",
        "You hold out the crescent amulet. The mist wraps around it like "
        "a child taking a mother's hand. The singing softens into a "
        "lullaby you never learned, and then into silence. When the mist "
        "fades, the amulet lies warm in your palm - a gift returned, a "
        "debt repaid. The shrine is quiet, though no one will ever know "
        "exactly why.",
        is_ending=True,
        ending_name="The Keeper's Daughter",
    ))
    add(StoryNode(
        "hollow_victory",
        "You strike through the mist. The song breaks into a single, "
        "terrible note and scatters like blown snow. The council will "
        "call you a hero, and Ryse will drink to your name - but some "
        "nights, on the road, you will hear a half-song in the wind and "
        "wonder what you could have sung instead.",
        is_ending=True,
        ending_name="A Hollow Victory",
    ))
    add(StoryNode(
        "fled_shrine",
        "You run until the shrine is a smudge of cold light behind you. "
        "Behind you, faint and patient, the singing continues. In "
        "Ashenbrook they will burn the shrine at dawn, and the song will "
        "move elsewhere - as songs do.",
        is_ending=True,
        ending_name="The Song Continues",
    ))
    add(StoryNode(
        "abandoned_quest",
        "You turn your back on the black door and do not look again. At "
        "dawn, smoke rises from the mountain, and the village celebrates "
        "a silence that does not quite feel like peace. You travel on, "
        "and the half-song follows you a little way before it lets you "
        "go.",
        is_ending=True,
        ending_name="Ashes in the Mist",
    ))
    add(StoryNode(
        "leave_village",
        "You take the south road under the stars and leave Ashenbrook "
        "and its grieving shrine behind. Whatever happened in the dark "
        "up there, it was never going to be your story to finish.",
        is_ending=True,
        ending_name="The Quiet Road",
    ))
    return nodes