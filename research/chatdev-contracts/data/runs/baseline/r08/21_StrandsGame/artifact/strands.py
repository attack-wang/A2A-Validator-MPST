'''
Strands — a word-segmentation puzzle game.
...description, commands, how to run...
'''
import random
import re
import sys
from itertools import islice
# ---------------------------------------------------------------------------
# Built-in reference dictionary (common English words) used only to decide
# whether a rejected merge is a "real word" (NYT-style feedback) or gibberish.
# ---------------------------------------------------------------------------
_DICTIONARY_TEXT = (
    "ACE ACT ADD AGE AGO AID AIM AIR ALL AND ANT ANY APE ARM ART ASH ASK ATE "
    ...
)
VALID_WORDS = frozenset(_DICTIONARY_TEXT.split())