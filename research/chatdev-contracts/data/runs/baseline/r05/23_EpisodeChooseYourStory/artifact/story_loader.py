'''
story_loader.py — Loads and validates story JSON files.
Validation checks that the story has a title/start, that every choice
target and on-enter reference points to an existing node, and that every
non-ending node has at least one choice while ending nodes declare an
ending_id. Raises StoryValidationError with a readable message on failure.
'''