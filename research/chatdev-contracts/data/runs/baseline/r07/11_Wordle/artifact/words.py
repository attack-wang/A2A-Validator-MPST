'''
words.py
Word data and word-list helpers.
- WORD_LIST:       pool of valid 5-letter guess words.
- WORD_LENGTH:     required guess length (5).
- load_words():    returns the list of valid words.
- get_daily_word(): deterministically picks the word of the day from the
  calendar date, so every player on the same day gets the same word.
'''
import datetime
WORD_LENGTH = 5
WORD_LIST = [
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
    "alike", "alive", "allow", "alone", "along", "alter", "among", "anger",
    "angle", "angry", "apart", "apple", "apply", "arena", "argue", "arise",
    "armor", "aroma", "array", "arrow", "aside", "asset", "audio", "audit",
    "avoid", "award", "aware", "badly", "baker", "basic", "basis", "beach",
    "began", "begin", "being", "below", "bench", "birth", "black", "blame",
    "blind", "block", "blood", "board", "boost", "booth", "bound", "brain",
    "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke",
    "brown", "build", "built", "buyer", "cable", "carry", "catch", "cause",
    "chain", "chair", "chart", "chase", "cheap", "check", "chest", "chief",
    "child", "chose", "civil", "claim", "class", "clean", "clear", "click",
    "cliff", "climb", "clock", "close", "coach", "coast", "color", "could",
    "count", "court", "cover", "craft", "crash", "cream", "crime", "cross",
    "crowd", "crown", "curve", "cycle", "daily", "dance", "dealt", "death",
    "debut", "delay", "depth", "doing", "doubt", "dozen", "draft", "drama",
    "drawn", "dream", "dress", "drill", "drink", "drive", "drove", "eager",
    "early", "earth", "eight", "elite", "empty", "enemy", "enjoy", "enter",
    "entry", "equal", "error", "event", "every", "exact", "exist", "extra",
    "faith", "false", "fault", "fiber", "field", "fifth", "fifty", "fight",
    "final", "first", "fixed", "flash", "fleet", "floor", "fluid", "focus",
    "force", "forth", "forty", "forum", "found", "frame", "fraud", "fresh",
    "front", "fruit", "fully", "funny", "giant", "given", "glass", "globe",
    "going", "grace", "grade", "grand", "grant", "grass", "great", "green",
    "gross", "group", "grown", "guard", "guess", "guest", "guide", "happy",
    "harsh", "heart", "heavy", "hence", "horse", "hotel", "house", "human",
    "ideal", "image", "index", "inner", "input", "issue", "joint", "judge",
    "known", "label", "large", "laser", "later", "laugh", "layer", "learn",
    "lease", "least", "leave", "legal", "level", "light", "limit", "local",
    "logic", "loose", "lower", "lucky", "lunch", "lying", "magic", "major",
    "maker", "march", "match", "maybe", "mayor", "meant", "media", "metal",
    "might", "minor", "minus", "mixed", "model", "money", "month", "moral",
    "motor", "mount", "mouse", "mouth", "movie", "music", "needs", "never",
    "newly", "night", "noise", "north", "noted", "novel", "nurse", "occur",
    "ocean", "offer", "often", "order", "other", "ought", "paint", "panel",
    "paper", "party", "peace", "phase", "phone", "photo", "piece", "pilot",
    "pitch", "place", "plain", "plane", "plant", "plate", "point", "pound",
    "power", "press", "price", "pride", "prime", "print", "prior", "prize",
    "proof", "proud", "prove", "queen", "quick", "quiet", "quite", "radio",
    "raise", "range", "rapid", "ratio", "reach", "ready", "refer", "right",
    "rival", "river", "robot", "rough", "round", "route", "royal", "rural",
    "scale", "scene", "scope", "score", "sense", "serve", "seven", "shall",
    "shape", "share", "sharp", "sheet", "shelf", "shell", "shift", "shirt",
    "shock", "shoot", "short", "shown", "sight", "since", "sixth", "sixty",
    "skill", "sleep", "slide", "small", "smart", "smile", "smoke", "solid",
    "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed",
    "spend", "spent", "split", "spoke", "sport", "staff", "stage", "stake",
    "stand", "start", "state", "steam", "steel", "stick", "still", "stock",
    "stone", "stood", "store", "storm", "story", "strip", "stuck", "study",
    "stuff", "style", "sugar", "suite", "super", "sweet", "table", "taken",
    "taste", "teach", "teeth", "thank", "theft", "their", "theme", "there",
    "these", "thick", "thing", "think", "third", "those", "three", "threw",
    "throw", "tight", "tired", "title", "today", "topic", "total", "touch",
    "tough", "tower", "track", "trade", "train", "treat", "trend", "trial",
    "tried", "truck", "truly", "trust", "truth", "twice", "under", "union",
    "unity", "until", "upper", "upset", "urban", "usage", "usual", "valid",
    "value", "video", "virus", "visit", "vital", "voice", "waste", "watch",
    "water", "wheel", "where", "which", "while", "white", "whole", "whose",
    "woman", "women", "world", "worry", "worse", "worst", "worth", "would",
    "wound", "write", "wrong", "wrote", "young", "youth", "zebra",
]
def load_words():
    """Return the list of valid guess words (lowercase, 5 letters)."""
    return list(WORD_LIST)
def get_daily_word(words):
    """
    Pick the daily word deterministically from today's date.
    Same word for all players on the same day; rotates at midnight.
    """
    day_index = datetime.date.today().toordinal() % len(words)
    return words[day_index]