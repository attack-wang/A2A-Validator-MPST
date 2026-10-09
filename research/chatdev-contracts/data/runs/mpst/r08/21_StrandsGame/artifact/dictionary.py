'''
dictionary.py
Bonus-word dictionary for the Strands puzzle.
Any concatenation of strands that is not a target word may still be
accepted as a "bonus" merge if it appears in this dictionary. The
dictionary ships with a built-in word list and optionally loads extra
words from a plain-text file (one word per line).
'''
import os
from typing import Set
# Built-in fallback list so the game works even without words.txt.
BUILTIN_WORDS = {
    "AND", "ARE", "ARM", "ART", "ATE", "BAD", "BAG", "BAN", "BAR", "BAT",
    "BEAM", "BEAN", "BEAT", "BELL", "BELT", "BEST", "BIRD", "BITE", "BOND",
    "BOOK", "BOOT", "BORN", "BOSS", "BOTH", "BOWL", "BURN", "BUS", "BUSH",
    "CAKE", "CALL", "CALM", "CAME", "CAMP", "CARD", "CARE", "CART", "CASE",
    "CASH", "CAST", "CELL", "CHAT", "CHIP", "CITY", "CLAP", "CLAY", "CLIP",
    "COAL", "COAT", "COIN", "COLD", "COMB", "COOK", "COOL", "COPY", "CORD",
    "CORE", "CORN", "COST", "CREW", "CROP", "DARK", "DATA", "DATE", "DAWN",
    "DAY", "DEAL", "DEAR", "DEEP", "DEER", "DESK", "DIAL", "DIET", "DISK",
    "DOCK", "DOES", "DONE", "DOOR", "DOSE", "DOWN", "DRAG", "DRAW", "DREW",
    "DROP", "DRUM", "DUAL", "DUCK", "DUST", "DUTY", "EACH", "EARN", "EASE",
    "EAST", "EASY", "EDGE", "EDIT", "ELSE", "EVEN", "EVER", "EXIT", "FACE",
    "FACT", "FAIL", "FAIR", "FALL", "FARM", "FAST", "FATE", "FEAR", "FEED",
    "FEET", "FELL", "FELT", "FILE", "FILL", "FILM", "FIND", "FINE", "FIRE",
    "FIRM", "FISH", "FIST", "FIVE", "FLAT", "FLEW", "FLOW", "FOLD", "FOLK",
    "FOND", "FOOD", "FOOL", "FOOT", "FORM", "FORT", "FOUR", "FREE", "FROG",
    "FROM", "FUEL", "FULL", "GAIN", "GAME", "GANG", "GAS", "GATE", "GAVE",
    "GEAR", "GIFT", "GIVE", "GLAD", "GOAL", "GOAT", "GOES", "GOLD", "GOLF",
    "GONE", "GOOD", "GRAB", "GRAY", "GREW", "GRIP", "GROW", "HAIR", "HALF",
    "HALL", "HAND", "HANG", "HARD", "HARM", "HATE", "HAVE", "HEAD", "HEAR",
    "HEAT", "HELD", "HELL", "HELP", "HERB", "HERE", "HERO", "HIDE", "HIGH",
    "HILL", "HINT", "HIT", "HOLD", "HOLE", "HOME", "HOPE", "HORN", "HOST",
    "HOUR", "HUGE", "HUNT", "HURT", "ICE", "IDEA", "INTO", "IRON", "ITEM",
    "JOBS", "JOIN", "JOKE", "JUMP", "JUST", "KEEP", "KEPT", "KEY", "KICK",
    "KIND", "KING", "KNEE", "KNEW", "KNIT", "KNOT", "KNOW", "LACK", "LAKE",
    "LAMP", "LAND", "LANE", "LAST", "LATE", "LAWN", "LAZY", "LEAD", "LEAF",
    "LEAGUE", "LEAN", "LEFT", "LEND", "LENS", "LESS", "LIFE", "LIFT", "LIKE",
    "LINE", "LION", "LIST", "LIVE", "LOAD", "LOAN", "LOCK", "LOG", "LONG",
    "LOOK", "LORD", "LOSS", "LOST", "LOTS", "LOUD", "LOVE", "LUCK", "MADE",
    "MAIL", "MAIN", "MAKE", "MALE", "MALL", "MAN", "MANY", "MAP", "MARK",
    "MASK", "MASS", "MATCH", "MATH", "MEAL", "MEAN", "MEAT", "MEET", "MENU",
    "MERE", "MESS", "MILD", "MILE", "MILK", "MIND", "MINE", "MISS", "MODE",
    "MOOD", "MOON", "MORE", "MOST", "MOVE", "MUCH", "MUST", "NAME", "NAVY",
    "NEAR", "NEAT", "NECK", "NEED", "NEWS", "NEXT", "NICE", "NINE", "NODE",
    "NONE", "NOON", "NOSE", "NOTE", "ONCE", "ONLY", "OPEN", "ORAL", "OURS",
    "OVAL", "OVER", "PACE", "PACK", "PAGE", "PAID", "PAIN", "PAIR", "PALE",
    "PALM", "PARK", "PART", "PASS", "PAST", "PATH", "PEAK", "PEEL", "PEN",
    "PEST", "PICK", "PIECE", "PIKE", "PILE", "PINE", "PINK", "PIPE", "PLAN",
    "PLAY", "PLOT", "PLUG", "PLUS", "POEM", "POET", "POLE", "POND", "POOL",
    "POOR", "PORT", "POSE", "POST", "POUR", "PRAY", "PULL", "PURE", "PUSH",
    "QUIT", "QUIZ", "RACE", "RACK", "RAFT", "RAIN", "RANK", "RARE", "RATE",
    "READ", "REAL", "RENT", "REST", "RICE", "RICH", "RIDE", "RING", "RISE",
    "RISK", "ROAD", "ROAR", "ROCK", "RODE", "ROLE", "ROLL", "ROOF", "ROOM",
    "ROOT", "ROPE", "ROSE", "ROSY", "RULE", "RUSH", "RUST", "SAFE", "SAID",
    "SAIL", "SAKE", "SALE", "SALT", "SAME", "SAND", "SAVE", "SEAL", "SEAT",
    "SEED", "SEEK", "SEEM", "SEEN", "SELF", "SELL", "SEND", "SENT", "SHIP",
    "SHOE", "SHOP", "SHOT", "SHOW", "SHUT", "SICK", "SIDE", "SIGN", "SILK",
    "SING", "SINK", "SITE", "SIZE", "SKIN", "SLIP", "SLOW", "SNAP", "SNOW",
    "SOAP", "SOCK", "SOFA", "SOFT", "SOIL", "SOLD", "SOLE", "SOME", "SONG",
    "SOON", "SORT", "SOUL", "SOUP", "SPIN", "SPOT", "STAR", "STAY", "STEM",
    "STEP", "STIR", "STOP", "SUCH", "SUIT", "SURE", "SURF", "SWAN", "SWIM",
    "TAIL", "TAKE", "TALE", "TALK", "TALL", "TANK", "TAPE", "TASK", "TAXI",
    "TEAM", "TEAR", "TELL", "TEND", "TENT", "TERM", "TEST", "TEXT", "THAN",
    "THAT", "THEM", "THEN", "THEY", "THIN", "THIS", "TIDE", "TIED", "TILE",
    "TIME", "TINY", "TIRE", "TOAD", "TOLD", "TONE", "TOOK", "TOOL", "TORE",
    "TOWN", "TRAP", "TREE", "TRIM", "TRIP", "TRUE", "TUNE", "TURN", "TWIN",
    "TYPE", "UNIT", "UPON", "URGE", "USED", "USER", "VARY", "VAST", "VERY",
    "VIEW", "VINE", "VISA", "VOID", "VOTE", "WADE", "WAGE", "WAIT", "WAKE",
    "WALK", "WALL", "WANT", "WARD", "WARM", "WARN", "WASH", "WAVE", "WEAK",
    "WEAR", "WEED", "WEEK", "WEPT", "WERE", "WEST", "WHAT", "WHEN", "WHOM",
    "WIDE", "WIFE", "WILD", "WILL", "WIND", "WINE", "WING", "WINK", "WIPE",
    "WIRE", "WISE", "WISH", "WITH", "WOOD", "WOOL", "WORD", "WORE", "WORK",
    "WORM", "WRAP", "YARD", "YARN", "YEAR", "YELL", "ZERO", "ZONE",
}
class WordDictionary:
    """Valid bonus-word dictionary; loads optional extra words from words.txt."""
    def __init__(self, extra_file: str = "words.txt") -> None:
        """Build the dictionary from BUILTIN_WORDS plus an optional extra file.
        Args:
            extra_file: path to a plain-text file with one word per line.
                Missing files are silently ignored so the game still runs.
        """
        self._words: Set[str] = set(BUILTIN_WORDS)
        if os.path.exists(extra_file):
            with open(extra_file, "r", encoding="utf-8") as fh:
                self._words |= {line.strip().upper() for line in fh if line.strip()}
    def is_valid(self, word: str) -> bool:
        """Return True when `word` (case-insensitive) is in the dictionary."""
        return word.upper() in self._words
    def __contains__(self, word: str) -> bool:
        """Allow `word in dictionary` syntax."""
        return self.is_valid(word)
    def __len__(self) -> int:
        """Number of words known by this dictionary."""
        return len(self._words)