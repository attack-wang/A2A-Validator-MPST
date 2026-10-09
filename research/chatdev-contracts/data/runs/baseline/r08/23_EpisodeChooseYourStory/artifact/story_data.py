'''
story_data.py
Structured story branches for "The Shattered Vale", an interactive
storytelling game. Every node is a dictionary with a title, narrative text,
and either:
  - 'choices': player decisions, each with an optional 'effects' dict that
    mutates GameState (relationships, items, flags, variables), or
  - 'auto': an ordered list of conditional transitions; the first branch
    whose conditions pass against GameState determines the next node.
    The final branch must have empty conditions as a fallback.
Nodes with "ending": True terminate the playthrough.
'''
def validate_story(story):
    """Check referential integrity of every branch; return list of errors."""
    errors = []
    if "start" not in story:
        errors.append("Story is missing its 'start' node.")
        return errors
    for node_id, node in story.items():
        if "text" not in node:
            errors.append(f"Node '{node_id}' is missing 'text'.")
        for i, choice in enumerate(node.get("choices", [])):
            if "text" not in choice or "next" not in choice:
                errors.append(f"Node '{node_id}' choice {i} missing 'text'/'next'.")
            elif choice["next"] not in story:
                errors.append(f"Node '{node_id}' choice {i} -> unknown node '{choice['next']}'.")
        for j, branch in enumerate(node.get("auto", [])):
            if "next" not in branch:
                errors.append(f"Node '{node_id}' auto {j} missing 'next'.")
            elif branch["next"] not in story:
                errors.append(f"Node '{node_id}' auto {j} -> unknown node '{branch['next']}'.")
    return errors
STORY = {
    "start": {
        "title": "The Shattered Vale",
        "text": (
            "Dawn breaks over the Shattered Vale, and with it come the Warden's horns.\n"
            "Your oldest friend Maren lies at the crossroads, her leg gashed open, while\n"
            "the Warden's torches snake down the northern ridge toward the sleeping\n"
            "village. Somewhere in that camp sits the heart-stone, the Vale's last\n"
            "protection. What do you do?"
        ),
        "choices": [
            {"text": "Kneel and tend to Maren's wound.",
             "next": "tend_maren",
             "effects": {"relationships": {"maren": 2}}},
            {"text": "Leave her briefly and scout the ridge for a path.",
             "next": "scout_ridge",
             "effects": {"variables": {"courage": 1}, "add_items": ["healing_salve"]}},
            {"text": "Run for the village and ring the alarm bell.",
             "next": "village",
             "effects": {"flags": {"alarmed_village": True}}},
        ],
    },
    "tend_maren": {
        "title": "A Friend's Debt",
        "text": (
            "You bind the gash with strips of your cloak. Maren grips your wrist.\n"
            "\"The Warden took the heart-stone,\" she whispers. \"Without it the Vale\n"
            "dies by winter.\" Her eyes search yours, waiting."
        ),
        "choices": [
            {"text": "\"Then we take it back. Together.\"",
             "next": "approach_warden",
             "effects": {"relationships": {"maren": 1}, "variables": {"courage": 1}}},
            {"text": "\"Stay hidden. I'll go alone.\"",
             "next": "approach_warden",
             "effects": {"relationships": {"maren": -1}}},
        ],
    },
    "scout_ridge": {
        "title": "The Ridge",
        "text": (
            "You climb through the wet bracken and count the Warden's fires: twelve,\n"
            "maybe more. In an abandoned healer's satchel you find a sealed healing\n"
            "salve. Below, the camp gate stands half-open in the dark."
        ),
        "choices": [
            {"text": "Slip down toward the camp gate.",
             "next": "approach_warden",
             "effects": {"variables": {"courage": 1}}},
            {"text": "Return and treat Maren with the salve.",
             "next": "tend_maren",
             "effects": {"relationships": {"maren": 1}}},
        ],
    },
    "village": {
        "title": "The Bell Tower",
        "text": (
            "The alarm bell tolls across the Vale. Doors open; spears are taken down\n"
            "from walls. The militia will march, but slowly, and Maren is still lying\n"
            "at the crossroads."
        ),
        "choices": [
            {"text": "Wait for the militia to gather.",
             "next": "fight_warden",
             "effects": {"variables": {"courage": -1}}},
            {"text": "Slip away before the militia forms up.",
             "next": "tend_maren",
             "effects": {"relationships": {"maren": 1}}},
        ],
    },
    "approach_warden": {
        "title": "The Warden's Camp",
        "text": (
            "The heart-stone glints inside an iron cage beside the Warden's tent.\n"
            "A guard steps into your path, spear leveled. There is no retreating now."
        ),
        "choices": [
            {"text": "Fight the guard head-on.",
             "next": "fight_warden"},
            {"text": "Bluff: claim you carry the Warden's own orders.",
             "next": "talk_guard"},
        ],
    },
    "talk_guard": {
        "title": "A Necessary Lie",
        "text": (
            "You square your shoulders and invent orders on the spot, naming ranks\n"
            "and roads you have never seen. The guard's spear does not move."
        ),
        "auto": [
            {"conditions": [{"type": "variable", "name": "courage", "op": ">=", "value": 2}],
             "next": "bluff_success"},
            {"conditions": [], "next": "bluff_fail"},
        ],
    },
    "bluff_success": {
        "title": "Steel Nerve",
        "text": (
            "The guard wavers, then salutes and waves you through. You lift the\n"
            "heart-stone from its cage and walk out of the camp without once\n"
            "looking back."
        ),
        "choices": [
            {"text": "Carry the stone to safety.",
             "next": "finale",
             "effects": {"variables": {"courage": 1}}},
        ],
    },
    "bluff_fail": {
        "title": "The Lie Collapses",
        "text": (
            "\"Orders?\" The guard's eyes narrow. \"The Warden gave no orders at\n"
            "dawn.\" The spear drops to bar your way. Only one road remains."
        ),
        "choices": [
            {"text": "Fight.",
             "next": "fight_warden"},
        ],
    },
    "fight_warden": {
        "title": "Steel and Firelight",
        "text": (
            "Steel rings against steel in the firelight. The guard is trained, and\n"
            "the Warden's men are waking all around you. How the fight goes depends\n"
            "on who you have become tonight."
        ),
        "auto": [
            {"conditions": [{"type": "variable", "name": "courage", "op": ">=", "value": 3}],
             "next": "victory_fight"},
            {"conditions": [{"type": "item", "item": "healing_salve", "op": "has"}],
             "next": "victory_salve"},
            {"conditions": [{"type": "flag", "name": "alarmed_village", "op": "is"}],
             "next": "victory_rescue"},
            {"conditions": [], "next": "ending_lost"},
        ],
    },
    "victory_fight": {
        "title": "Fearless",
        "text": (
            "You fight without hesitation, every step already decided. The guard\n"
            "breaks and runs, and the camp's shouts fade behind you."
        ),
        "choices": [
            {"text": "Slip into the dark with the stone.",
             "next": "finale"},
        ],
    },
    "victory_salve": {
        "title": "A Healer's Luck",
        "text": (
            "A blade opens your arm, but you stagger back, smear the healing salve\n"
            "into the wound, and keep your feet. The guard hesitates at your\n"
            "sudden recovery, and that hesitation is enough."
        ),
        "choices": [
            {"text": "Seize the stone and run.",
             "next": "finale"},
        ],
    },
    "victory_rescue": {
        "title": "The Militia Arrives",
        "text": (
            "Horns answer from the village: the militia has come at last. The\n"
            "Warden's men scatter into the trees, and the cage stands unguarded."
        ),
        "choices": [
            {"text": "Break the cage open.",
             "next": "finale"},
        ],
    },
    "finale": {
        "title": "The Heart of the Vale",
        "text": (
            "Dawn is fully up now. The heart-stone hums against your palms, warm\n"
            "as a living thing. Beyond the ridge, the Vale is waiting to learn\n"
            "what kind of night you had."
        ),
        "auto": [
            {"conditions": [{"type": "relationship", "name": "maren", "op": ">=", "value": 2}],
             "next": "ending_reunion"},
            {"conditions": [], "next": "ending_alone"},
        ],
    },
    "ending_reunion": {
        "title": "Ending: Two Sets of Footprints",
        "text": (
            "You find Maren waiting at the crossroads, pale but smiling. Together\n"
            "you set the heart-stone back in its hollow, and green light runs\n"
            "through the Vale like spring arriving early.\n"
            "\"Next time,\" she says, leaning on your shoulder, \"we scout the ridge\n"
            "together.\" The Vale lives, and so does the friendship that saved it."
        ),
        "ending": True,
    },
    "ending_alone": {
        "title": "Ending: The Quiet Return",
        "text": (
            "You set the heart-stone back in its hollow alone, and the Vale is\n"
            "saved. But at the crossroads there is only blood on the grass where\n"
            "Maren lay; she has limped off toward the hills without you.\n"
            "The stone is warm in your hands. The silence is colder."
        ),
        "ending": True,
    },
    "ending_lost": {
        "title": "Ending: Ashes Before Winter",
        "text": (
            "The fight goes out of you the way the firelight does, slowly and then\n"
            "all at once. The Warden keeps the heart-stone, and by winter the Vale\n"
            "is grey ash and empty doorways.\n"
            "They will tell stories about the one who tried. They will not remember\n"
            "your name."
        ),
        "ending": True,
    },
}