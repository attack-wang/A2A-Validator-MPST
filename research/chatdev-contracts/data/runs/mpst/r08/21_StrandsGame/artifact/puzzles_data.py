'''
puzzles_data.py
Puzzle definitions for the Strands word-segmentation game.
Each puzzle defines:
    name        -- display title of the puzzle
    theme       -- hint shown to the player
    difficulty  -- Easy / Medium / Hard label
    description -- one-line flavour text
    core_word   -- the special "spangram-like" word worth extra points
    words       -- mapping of target word -> list of strand fragments whose
                   concatenation (in order) rebuilds the word exactly.
Strand fragments are shuffled onto the board; the player must recombine
them in the correct order to form each target word.
'''
PUZZLES = [
    {
        "name": "Word Workshop",
        "theme": "Building blocks of language",
        "difficulty": "Easy",
        "description": "Recombine the fragments to rebuild the vocabulary of language itself.",
        "core_word": "STRANDS",
        "words": {
            "STRANDS": ["STR", "AND", "S"],
            "SEGMENT": ["SEG", "MENT"],
            "LETTER": ["LET", "TER"],
            "SYLLABLE": ["SYL", "LA", "BLE"],
            "PHRASE": ["PHR", "ASE"],
        },
    },
    {
        "name": "Night Sky",
        "theme": "Things you see when you look up",
        "difficulty": "Medium",
        "description": "The heavens above, split into drifting fragments.",
        "core_word": "CONSTELLATION",
        "words": {
            "CONSTELLATION": ["CONSTEL", "LA", "TION"],
            "COMET": ["COM", "ET"],
            "GALAXY": ["GAL", "AX", "Y"],
            "NEBULA": ["NEB", "U", "LA"],
            "ORBIT": ["OR", "BIT"],
            "METEOR": ["METE", "OR"],
        },
    },
    {
        "name": "In the Kitchen",
        "theme": "Tools and tastes of cooking",
        "difficulty": "Medium",
        "description": "Every dish begins with pieces on the counter.",
        "core_word": "SPATULA",
        "words": {
            "SPATULA": ["SPA", "TU", "LA"],
            "WHISK": ["WH", "ISK"],
            "LADLE": ["LAD", "LE"],
            "SIMMER": ["SIM", "MER"],
            "GARNISH": ["GAR", "NISH"],
            "RECIPE": ["REC", "IPE"],
        },
    },
    {
        "name": "Ocean Depths",
        "theme": "Life beneath the waves",
        "difficulty": "Hard",
        "description": "Fragments adrift in deep water, waiting to surface as words.",
        "core_word": "BIOLUMINESCENCE",
        "words": {
            "BIOLUMINESCENCE": ["BIO", "LUMI", "NES", "CENCE"],
            "CORAL": ["COR", "AL"],
            "TRENCH": ["TREN", "CH"],
            "PLANKTON": ["PLANK", "TON"],
            "ANEMONE": ["ANE", "MO", "NE"],
            "CURRENT": ["CUR", "RENT"],
            "KELP": ["KEL", "P"],
        },
    },
]