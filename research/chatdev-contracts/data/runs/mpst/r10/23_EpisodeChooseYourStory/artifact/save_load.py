'''
Persistence layer and story data for "The Whispering Vale".
'''
import json
import os
STORY = {
    "start": {
        "text": (
            "Dusk settles over the Whispering Vale. You stand at the edge of "
            "an ancient forest, where the trees murmur in a tongue older than "
            "memory. A worn path forks ahead: one branch leads toward a distant "
            "village glow, the other plunges straight into the whispering woods."
        ),
        "choices": [
            {
                "text": "Follow the lantern light toward the village.",
                "effects": {"set_flags": ["met_villagers"]},
                "next": "village",
            },
            {
                "text": "Brave the whispering woods directly.",
                "effects": {"variables": {"courage": 1}},
                "next": "forest_path",
            },
        ],
    },
    ...
}