'''
puzzles.py — Puzzle definitions and the shared word dictionary for the Strands game.
Each puzzle definition is a dict with keys:
    title     : display name of the puzzle
    theme     : hint shown to the player
    targets   : list of words the player must form (display form)
    strands   : list of strand fragments; their letters must exactly cover
                every target letter (each strand used at most once)
    spangram  : optional special target highlighted on completion
PUZZLES is consumed by main.choose_puzzle(); DICTIONARY backs the
MergeValidator so near-miss merges can still be recognised as real words.
'''
PUZZLES = [
    {
        "title": "Word Weave",
        "theme": "Compound words: pair the fragments to build each word",
        "targets": ["SUNFLOWER", "RAINDROP", "NOTEBOOK", "CUPCAKE"],
        "strands": ["SUN", "FLOWER", "RAIN", "DROP", "NOTE", "BOOK", "CUP", "CAKE"],
        "spangram": "NOTEBOOK",
    },
    {
        "title": "Sky Watch",
        "theme": "Things you may see above your head",
        "targets": ["FOOTBALL", "SNOWMAN", "RAINBOW", "SUNSHINE"],
        ...
    },
]