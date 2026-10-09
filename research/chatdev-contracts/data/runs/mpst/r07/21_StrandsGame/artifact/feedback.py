'''
feedback.py
Defines the feedback system for the Strands puzzle game.
Contains FeedbackType (an enumeration of all feedback categories),
the Feedback dataclass carrying a message/detail pair, and a small
embedded dictionary of common English words used to detect "near
misses" (real words that are simply not part of the puzzle).
'''
from enum import Enum, auto
from dataclasses import dataclass
class FeedbackType(Enum):
    """Categories of feedback the game can produce."""
    SUCCESS = auto()      # a valid puzzle word was formed
    KEY_WORD = auto()     # the special "spangram"-like word was formed
    ERROR = auto()        # invalid input / not a word
    NEAR_MISS = auto()    # a real English word, but not a puzzle word
    INFO = auto()         # neutral information
    HINT = auto()         # hint content
    WARNING = auto()      # recoverable user mistake (bad indices, etc.)
    VICTORY = auto()      # puzzle fully solved
@dataclass
class Feedback:
    """A single unit of game feedback: a type, a message, optional detail."""
    ftype: FeedbackType
    message: str
    detail: str = ""
    def __str__(self):
        """Return a human-readable one-line rendering of the feedback."""
        if self.ftype in (FeedbackType.SUCCESS, FeedbackType.KEY_WORD, FeedbackType.VICTORY):
            mark = "✓"
        elif self.ftype in (FeedbackType.ERROR, FeedbackType.WARNING, FeedbackType.NEAR_MISS):
            mark = "✗"
        else:
            mark = "ℹ"
        text = f"[{mark}] {self.message}"
        if self.detail:
            text += f" ({self.detail})"
        return text
# A compact set of common English words used to detect "near misses":
# when a player concatenates strands into a real word that simply is not
# one of the puzzle's target words, we can say so instead of a flat error.
COMMON_WORDS = {
    "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER",
    "WAS", "ONE", "OUR", "DAY", "HAD", "HAS", "HIM", "HIS", "HOW", "MAN",
    "NEW", "NOW", "OLD", "SEE", "TWO", "WAY", "WHO", "BOY", "DID", "ITS",
    "LET", "PUT", "SAY", "SHE", "TOO", "USE", "CAT", "DOG", "SUN", "RUN",
    "EAT", "BIG", "GET", "GOT", "YES", "NO", "GO", "UP", "ON", "IN", "AT",
    "TO", "IT", "IS", "AS", "BE", "BY", "WE", "OR", "AN", "AM", "IF", "SO",
    "DO", "OF", "ME", "MY", "HE", "AH", "OH", "HI", "OK", "WORD", "GAME",
    "PLAY", "TIME", "YEAR", "PEOPLE", "WATER", "LAND", "HOME", "HAND",
    "NIGHT", "LIFE", "WORLD", "SCHOOL", "STATE", "FAMILY", "STUDENT",
    "GROUP", "COUNTRY", "PROBLEM", "HAND", "PART", "PLACE", "CASE", "WEEK",
    "COMPANY", "SYSTEM", "PROGRAM", "QUESTION", "WORK", "GOVERNMENT",
    "NUMBER", "NIGHT", "POINT", "HOME", "WATER", "ROOM", "MOTHER", "AREA",
    "MONEY", "STORY", "FACT", "MONTH", "LOT", "RIGHT", "STUDY", "BOOK",
    "EYE", "JOB", "WORD", "BUSINESS", "ISSUE", "SIDE", "KIND", "HEAD",
    "HOUSE", "SERVICE", "FRIEND", "FATHER", "POWER", "HOURLY", "END",
    "TREE", "STONE", "RIVER", "OCEAN", "BEACH", "CLOUD", "RAIN", "SNOW",
    "WIND", "FIRE", "EARTH", "LIGHT", "DARK", "BLACK", "WHITE", "GREEN",
    "BLUE", "RED", "YELLOW", "PURPLE", "ORANGE", "PINK", "BROWN", "GRAY",
    "SMALL", "LARGE", "GREAT", "LONG", "SHORT", "HIGH", "LOW", "GOOD",
    "BAD", "HOT", "COLD", "WARM", "COOL", "FAST", "SLOW", "EARLY", "LATE",
    "FIRST", "LAST", "NEXT", "SAME", "DIFFERENT", "OWN", "OTHER", "MANY",
    "SOME", "FEW", "MOST", "MORE", "LESS", "MUCH", "EVERY", "EACH", "ANY",
    "BOTH", "HALF", "WHOLE", "FULL", "EMPTY", "OPEN", "CLOSE", "START",
    "STOP", "BEGIN", "FINISH", "HELP", "GIVE", "TAKE", "MAKE", "KNOW",
    "THINK", "SAY", "TELL", "ASK", "ANSWER", "COME", "GO", "WALK", "SIT",
    "STAND", "LOOK", "SEE", "WATCH", "HEAR", "LISTEN", "SPEAK", "TALK",
    "READ", "WRITE", "DRAW", "PAINT", "SING", "DANCE", "JUMP", "SWIM",
    "FLY", "SLEEP", "WAKE", "DREAM", "LOVE", "HATE", "LIKE", "WANT",
    "NEED", "HAVE", "HOLD", "KEEP", "LEAVE", "STAY", "WAIT", "FIND",
    "LOSE", "WIN", "TRY", "USE", "WORK", "REST", "EAT", "DRINK", "COOK",
    "BAKE", "CUT", "BREAK", "FIX", "BUILD", "MAKE", "GROW", "SHOW",
    "HIDE", "SEND", "BRING", "CARRY", "PUSH", "PULL", "TURN", "MOVE",
    "WORD", "LETTER", "SENTENCE", "PAGE", "LINE", "MARK", "NOTE", "SIGN",
    "NAME", "CALL", "VOICE", "SOUND", "MUSIC", "SONG", "TUNE", "BEAT",
    "STAR", "MOON", "SKY", "SEA", "HILL", "VALLEY", "FIELD", "FARM",
    "ROAD", "PATH", "STREET", "BRIDGE", "DOOR", "WINDOW", "WALL", "ROOF",
    "FLOOR", "TABLE", "CHAIR", "BED", "DESK", "BOX", "BAG", "CUP", "PLATE",
    "SPOON", "KNIFE", "FORK", "KEY", "LOCK", "CLOCK", "WATCH", "PHONE",
    "MAIL", "CARD", "PAPER", "PEN", "PENCIL", "BOOK", "MAP", "PICTURE",
    "PHOTO", "GIFT", "TOY", "BALL", "KITE", "BOAT", "SHIP", "TRAIN",
    "PLANE", "CAR", "BUS", "BIKE", "WHEEL", "ROAD", "TRIP", "JOURNEY",
    "WALK", "RUN", "JUMP", "CLIMB", "FALL", "RISE", "DROP", "LIFT",
    "CATCH", "THROW", "HIT", "TOUCH", "FEEL", "SMELL", "TASTE", "SWEET",
    "SOUR", "SALTY", "BITTER", "FRESH", "OLD", "YOUNG", "TALL", "SHORT",
    "THIN", "THICK", "SOFT", "HARD", "SMOOTH", "ROUGH", "WET", "DRY",
    "HEAVY", "LIGHT", "LOUD", "QUIET", "BRIGHT", "CLEAN", "DIRTY",
    "SAFE", "DANGER", "RICH", "POOR", "HAPPY", "SAD", "ANGRY", "CALM",
    "TIRED", "AWAKE", "STRONG", "WEAK", "BRAVE", "AFRAID", "KIND",
    "MEAN", "POLITE", "RUDE", "FUNNY", "SERIOUS", "BUSY", "FREE",
    "TRUE", "FALSE", "REAL", "FAKE", "EASY", "HARD", "SIMPLE", "COMPLEX",
    "CLEAR", "UNCLEAR", "SURE", "MAYBE", "PERHAPS", "ALWAYS", "NEVER",
    "OFTEN", "SOMETIMES", "SOON", "LATER", "TODAY", "TOMORROW", "YESTERDAY",
    "MORNING", "AFTERNOON", "EVENING", "MIDNIGHT", "NOON", "DAWN", "DUSK",
    "SPRING", "SUMMER", "AUTUMN", "FALL", "WINTER", "JANUARY", "FEBRUARY",
    "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER",
    "OCTOBER", "NOVEMBER", "DECEMBER", "MONDAY", "TUESDAY", "WEDNESDAY",
    "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY", "WEEKEND", "HOLIDAY",
    "BIRTHDAY", "PARTY", "WEDDING", "MEETING", "CLASS", "LESSON", "TEST",
    "GAME", "SPORT", "TEAM", "PLAYER", "COACH", "REFEREE", "GOAL",
    "SCORE", "WIN", "LOSE", "TIE", "MATCH", "RACE", "SWIM", "RUN",
    "WALK", "HIKE", "CLIMB", "DANCE", "SING", "PLAY", "FUN", "JOY",
    "SMILE", "LAUGH", "CRY", "TEAR", "HUG", "KISS", "WAVE", "NOD",
    "HAND", "FOOT", "ARM", "LEG", "HEAD", "FACE", "EYE", "EAR", "NOSE",
    "MOUTH", "TOOTH", "TONGUE", "LIP", "CHEEK", "CHIN", "NECK", "SHOULDER",
    "BACK", "CHEST", "HEART", "BRAIN", "BONE", "BLOOD", "SKIN", "HAIR",
    "FINGER", "THUMB", "KNEE", "ELBOW", "ANKLE", "WRIST", "HIP", "HEEL",
}
def is_common_word(text):
    """Return True if `text` (case-insensitive) is a known common English word."""
    return text.upper() in COMMON_WORDS