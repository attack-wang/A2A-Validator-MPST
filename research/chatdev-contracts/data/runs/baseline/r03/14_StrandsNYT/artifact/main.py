def generate_puzzle(theme_name):
    theme = THEMES[theme_name]
    spangram = theme["spangram"]
    words = list(theme["words"])
    # validate total length
    ...
    for attempt in range(MAX_ATTEMPTS):
        placements = partition(...)
        if placements: 
            grid = assign_letters(placements)
            return grid, placements
    return None