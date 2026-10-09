'''
puzzles_data.py - Puzzle definitions for the Strands word-segmentation game.
Each puzzle contains a title, theme, and entries. Each entry defines a target
word/phrase and the strand fragments that combine (in order) to form it.
An entry may be flagged as a "spangram" (special highlight target).
'''
PUZZLES = [
    {
        "title": "In the Garden",
        "theme": "Things you find in a garden",
        "entries": [
            {"word": "CATERPILLAR", "strands": ["CAT", "ERPIL", "LAR"]},
            {"word": "SUNFLOWER", "strands": ["SUN", "FLOW", "ER"]},
            {"word": "GREENHOUSE", "strands": ["GREEN", "HOUSE"]},
            {"word": "WATERING CAN", "strands": ["WATER", "ING", "CAN"], "spangram": True},
            {"word": "LADYBUG", "strands": ["LADY", "BUG"]},
            {"word": "BIRDBATH", "strands": ["BIRD", "BATH"]},
        ],
    },
    {
        "title": "In the Kitchen",
        "theme": "Tools and items found in a kitchen",
        "entries": [
            {"word": "CUTTINGBOARD", "strands": ["CUT", "TING", "BOARD"]},
            {"word": "SPATULA", "strands": ["SPA", "TULA"]},
            {"word": "MICROWAVE", "strands": ["MICRO", "WAVE"]},
            {"word": "DISHWASHER", "strands": ["DISH", "WASH", "ER"]},
            {"word": "REFRIGERATOR", "strands": ["RE", "FRIGER", "ATOR"], "spangram": True},
            {"word": "TEAKETTLE", "strands": ["TEA", "KET", "TLE"]},
        ],
    },
]