'''
save_manager.py — Persists and restores GameState as JSON files.
Saves are written to a directory (default "saves") with timestamps in the
filename so multiple playthroughs can coexist. load() restores a GameState
from a previously written file.
'''