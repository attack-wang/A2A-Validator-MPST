'''
wordlist.py
Contains the dictionary of valid 5-letter words and helpers to select
the daily word (deterministic per calendar date) or a random word.
Robustness notes:
  - The word list is validated at import time (length, lowercase a-z,
    uniqueness) so a corrupted dictionary fails fast with a clear message.
  - The allowed-letter set is defined locally as _ALLOWED_LETTERS so the
    import-time validation no longer references an undefined name.
'''
import datetime
import random
WORD_LENGTH = 5
_ALLOWED_LETTERS = set("abcdefghijklmnopqrstuvwxyz")
# Sorted list of common 5-letter English words (all lowercase).
WORDS = sorted([
    "about", "above", "abuse", "actor", "acute", "adapt", "admit", "adopt",
    "adore", "adult", "after", "again", "agent", "agree", "ahead", "alarm",
    "album", "alert", "alien", "alike", "alive", "allow", "alone", "along",
    "alter", "among", "anger", "angle", "angry", "ankle", "apart", "apple",
    "apply", "arena", "argue", "arise", "armor", "aroma", "arrow", "aside",
    "asset", "atlas", "audio", "audit", "avoid", "awake", "award", "aware",
    "badly", "baker", "basic", "beach", "began", "begin", "being", "below",
    "bench", "berry", "birth", "black", "blade", "blame", "blank", "blast",
    "bleak", "blend", "bless", "blind", "block", "blood", "bloom", "board",
    "boast", "bonus", "boost", "booth", "bound", "brain", "brand", "brave",
    "bread", "break", "breed", "brief", "bring", "broad", "broke", "brown",
    "brush", "build", "built", "bunch", "burst", "buyer", "cabin", "cable",
    "candy", "cargo", "carry", "catch", "cause", "chain", "chair", "chalk",
    "charm", "chart", "chase", "cheap", "check", "cheer", "chess", "chest",
    "chief", "child", "chill", "chose", "claim", "class", "clean", "clear",
    "clerk", "click", "cliff", "climb", "cling", "clock", "close", "cloud",
    "coach", "coast", "color", "comic", "coral", "couch", "could", "count",
    "court", "cover", "crane", "crash", "crawl", "crazy", "cream", "creek",
    "crest", "crime", "cross", "crowd", "crown", "crude", "curve", "cycle",
    "daily", "dance", "dated", "dealt", "death", "debut", "decay", "delay",
    "dense", "depth", "devil", "diary", "dirty", "disco", "ditch", "dizzy",
    "doubt", "dozen", "draft", "drain", "drama", "drank", "dream", "dress",
    "drill", "drink", "drive", "drove", "drown", "dryer", "eager", "eagle",
    "early", "earth", "eight", "elite", "empty", "enemy", "enjoy", "enter",
    "entry", "equal", "error", "event", "every", "exact", "exist", "extra",
    "faith", "false", "fault", "favor", "feast", "fence", "fever", "fewer",
    "fiber", "field", "fifth", "fifty", "fight", "final", "first", "flame",
    "flash", "fleet", "flesh", "float", "flood", "floor", "flour", "fluid",
    "flute", "focus", "force", "forge", "forth", "forty", "forum", "found",
    "frame", "fraud", "fresh", "fried", "front", "frost", "fruit", "fully",
    "funny", "giant", "given", "glass", "globe", "glory", "glove", "going",
    "goose", "grace", "grade", "grain", "grand", "grant", "grape", "graph",
    "grasp", "grass", "grave", "great", "green", "greet", "group", "guard",
    "guess", "guest", "guide", "habit", "happy", "harsh", "heart", "heavy",
    "hence", "hobby", "honey", "honor", "horse", "hotel", "house", "human",
    "humor", "ideal", "image", "index", "inner", "input", "issue", "ivory",
    "jelly", "jewel", "joint", "judge", "juice", "jumbo", "kneel", "knife",
    "knock", "known", "label", "labor", "laser", "later", "laugh", "layer",
    "learn", "lease", "least", "leave", "legal", "lemon", "level", "light",
    "limit", "linen", "liver", "local", "logic", "loose", "lorry", "loyal",
    "lucky", "lunch", "lying", "magic", "major", "maker", "mango", "maple",
    "march", "match", "maybe", "mayor", "meant", "medal", "media", "melon",
    "mercy", "merge", "merit", "metal", "meter", "might", "minor", "minus",
    "mixed", "model", "moist", "money", "month", "moral", "motor", "mount",
    "mouse", "mouth", "movie", "music", "naive", "nerve", "never", "newly",
    "night", "noble", "noise", "north", "noted", "novel", "nurse", "occur",
    "ocean", "offer", "often", "olive", "onion", "onset", "opera", "orbit",
    "order", "organ", "other", "ought", "outer", "owner", "paint", "panel",
    "panic", "paper", "pasta", "patch", "pause", "peace", "pearl", "pedal",
    "penny", "phase", "phone", "photo", "piano", "piece", "pilot", "pinch",
    "pitch", "pizza", "place", "plain", "plane", "plant", "plate", "plaza",
    "plead", "plenty", ... 
])