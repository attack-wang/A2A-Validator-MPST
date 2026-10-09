STORY = {
    "start": {
        "text": "...",
        "choices": [
            {"text": "Enter the vale at once, while the light lasts.", "next": "vale_dusk", "effects": {"set_flags": {"entered_at_dusk": True}, "adjust_variables": {"courage": 1}}},
            {"text": "Visit Elder Maren's hut before descending.", "next": "maren_hut", "effects": {"adjust_relationships": {"maren": 2}}},
        ],
    },
    ...
}