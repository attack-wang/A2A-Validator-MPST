"""Story data for 'The Hollow Crown'.

Structure: node id -> {"text": str, "choices": [...], "ending": bool (endings only)}
Each choice: {"label", "next", optional "effects", optional "if" condition}.
Conditions: {"item": name} | {"min": {var: v}} | {"max": {var: v}} |
            {"eq": {var: v}} | a list of these (all must hold).
Effects: {"gain": [items], "lose": [items], "add": {var: delta}, "set": {var: val}}.
"""

START = "crossroads"

STORY = {
    "crossroads": {
        "text": "Dusk settles over the crossroads. A cloaked stranger warms her hands at a small fire, and far to the east the lights of a village flicker. Ahead, the whispering forest swallows the old road that leads to Hollow Castle, where the cursed crown waits.",
        "choices": [
            {"label": "Take the old road into the whispering forest.",
             "next": "forest_edge", "effects": {"add": {"courage": 1}}},
            {"label": "Approach the stranger at the fire.", "next": "stranger"},
            {"label": "Walk toward the village lights.", "next": "village"},
        ],
    },
    "stranger": {
        "text": "The stranger lowers her hood: a scout named Mira, whose sister was taken by the castle's curse. She watches you warily, a hooded lantern at her feet.",
        "choices": [
            {"label": "Share your bread and listen to her tale.",
             "next": "mira_friend",
             "effects": {"add": {"trust": 1}, "gain": ["lantern"]}},
            {"label": "Keep your distance and press on alone.",
             "next": "forest_edge"},
        ],
    },
    "mira_friend": {
        "text": "Mira smiles for the first time in weeks and presses her lantern into your hands. 'The forest is kind only to those who carry light,' she says. 'Let me come with you.'",
        "choices": [
            {"label": "Let Mira join your quest.",
             "next": "forest_edge",
             "effects": {"add": {"trust": 1}, "set": {"companion": 1}}},
            {"label": "Travel alone, but keep the lantern.",
             "next": "forest_edge"},
        ],
    },
    "forest_edge": {
        "text": "The forest looms, branches knitted tight as a vault. Somewhere within stands the hollow oak, and beyond it the black towers of Hollow Castle.",
        "choices": [
            {"label": "Enter the forest depths.", "next": "forest_depths"},
            {"label": "Circle around to the village instead.", "next": "village"},
        ],
    },
    "forest_depths": {
        "text": "Roots twist like written runes. You find the hollow oak, its trunk split by an old wound, and beyond it a path climbing toward the castle gate.",
        "choices": [
            {"label": "Search the hollow oak.", "next": "hollow_oak"},
            {"label": "Press on toward the castle.", "next": "castle_gate"},
        ],
    },
    "hollow_oak": {
        "text": "The hollow breathes cold air. Something glints deep inside, out of sight.",
        "choices": [
            {"label": "Hold your lantern into the hollow.",
             "if": {"item": "lantern"},
             "next": "find_key", "effects": {"gain": ["iron_key"]}},
            {"label": "Reach into the hollow blindly.", "next": "snake_bite"},
        ],
    },
    "find_key": {
        "text": "By lantern-light you draw out a cold iron key stamped with the castle's seal. The forest seems to exhale around you.",
        "choices": [
            {"label": "Continue to the castle gate.", "next": "castle_gate"},
        ],
    },
    "snake_bite": {
        "text": "Fangs sink into your wrist. You wrench free, bleeding, as something scaled slides away into the dark. The key remains lost to the hollow.",
        "choices": [
            {"label": "Bind the wound and limp toward the castle.",
             "next": "castle_gate"},
        ],
    },
    "village": {
        "text": "The village of Ashford huddles behind a palisade. In the tavern hall, a grey elder sits beneath a carving of the crown, eyes closed.",
        "choices": [
            {"label": "Ask the elder about the crown.", "next": "elder_tale"},
            {"label": "Rest quietly at the inn.", "next": "inn"},
        ],
    },
    "elder_tale": {
        "text": "The elder opens one eye. 'The crown grants a wish to whoever breaks it, and a kingdom to whoever wears it. Every wearer so far has become its puppet.'",
        "choices": [
            {"label": "Promise to break the curse, not claim it.",
             "next": "vow", "effects": {"add": {"trust": 1}}},
            {"label": "Say you will take the crown for yourself.",
             "next": "elder_warns"},
        ],
    },
    "vow": {
        "text": "The elder presses a blessing to your brow. 'Then go with Ashford's hope behind you. Hearts bound to a promise open doors that keys cannot.'",
        "choices": [
            {"label": "Set out for the castle.", "next": "castle_gate"},
        ],
    },
    "elder_warns": {
        "text": "The elder's face hardens. 'Then you are no better than the last thief. Go, and learn what the crown does to grasping hands.'",
        "choices": [
            {"label": "Set out for the castle anyway.", "next": "castle_gate"},
        ],
    },
    "inn": {
        "text": "You sleep badly and wake before dawn, the crown's legend gnawing at you. There is nothing left but to go and see it yourself.",
        "choices": [
            {"label": "Continue to the castle at first light.",
             "next": "castle_gate"},
        ],
    },
    "castle_gate": {
        "text": "Hollow Castle rises against the stars. Its rusted gate is locked, and cold light leaks from the throne room window above.",
        "choices": [
            {"label": "Unlock the gate with the iron key.",
             "if": {"item": "iron_key"}, "next": "throne_room"},
            {"label": "Force the rusted gate open.",
             "next": "gate_break", "effects": {"add": {"courage": 1}}},
            {"label": "Turn back and abandon the quest.",
             "next": "ending_turn_back"},
        ],
    },
    "gate_break": {
        "text": "You set your shoulder to the gate until the hinges scream and give. You squeeze through into the courtyard, palms torn but unbroken.",
        "choices": [
            {"label": "Climb the stairs to the throne room.",
             "next": "throne_room"},
        ],
    },
    "throne_room": {
        "text": "On the throne of black stone rests the Hollow Crown, whispering your name in a hundred stolen voices. It is warmer than it should be, and it wants to be worn.",
        "choices": [
            {"label": "Shatter the crown with Mira at your side.",
             "if": [{"min": {"trust": 2}}, {"eq": {"companion": 1}}],
             "next": "ending_true_break"},
            {"label": "Shatter the crown alone.",
             "if": {"max": {"trust": 1}}, "next": "ending_lone_break"},
            {"label": "Place the crown upon your own brow.",
             "next": "ending_claim"},
            {"label": "Offer the crown to Mira.",
             "if": {"eq": {"companion": 1}}, "next": "ending_share"},
        ],
    },
    "ending_true_break": {
        "text": "Mira sets her hands over yours and together you bring the crown down against the throne's edge. It splits like a bell, and every stolen voice sighs free. Dawn finds you both walking home, unburdened, the forest whispering thanks instead of warnings.",
        "ending": True,
    },
    "ending_lone_break": {
        "text": "You smash the crown alone. The curse breaks, but no one witnesses it, and the wish it owed goes unclaimed. You leave Hollow Castle victorious and utterly by yourself, wondering which of the two weighs more.",
        "ending": True,
    },
    "ending_claim": {
        "text": "The crown settles onto your brow like a returning key. The whispers fall silent, because they no longer need to speak. Years later, villagers tell of a watchful king in Hollow Castle who never ages, and travellers hurry past the crossroads without stopping.",
        "ending": True,
    },
    "ending_share": {
        "text": "You kneel and offer Mira the crown. She stares, then laughs through tears and hurls it from the window into the moat, where the water swallows its whispering. 'The wish was never the point,' she says. Together you walk out of Hollow Castle as the curse dies behind you.",
        "ending": True,
    },
    "ending_turn_back": {
        "text": "You turn your back on the castle and its whispering crown. The curse endures, the forest keeps its secrets, and you live a long, ordinary life occasionally waking at night to wonder what might have been.",
        "ending": True,
    },
}