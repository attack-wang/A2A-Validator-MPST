"""Sound synthesis and playback with graceful fallbacks.
Sounds are synthesized procedurally with numpy when available; if numpy or
the pygame mixer is missing/unavailable, dummy sounds keep the game playable.
"""
import numpy as np  # wrapped below