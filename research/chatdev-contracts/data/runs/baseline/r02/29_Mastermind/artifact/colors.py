'''
colors.py
Color palette definitions and small helpers for the Mastermind game.
Internally, colors are represented by single digit characters ('1'..'6')
so the player can type them easily on the keyboard. This module maps those
codes to human-readable color names and validates player input.
'''
from config import NUM_COLORS
# Digit code -> display name for the standard 6-color palette.
COLOR_NAMES = {
    '1': 'Red',
    '2': 'Blue',
    '3': 'Green',
    '4': 'Yellow',
    '5': 'Orange',
    '6': 'Purple',
}
# Extra names in case NUM_COLORS is raised beyond 6.
EXTRA_COLOR_NAMES = ['Pink', 'Brown', 'Cyan', 'White', 'Black', 'Teal']
def valid_codes():
    """Return the list of valid color codes ('1' .. str(NUM_COLORS))."""
    return [str(i) for i in range(1, NUM_COLORS + 1)]
def color_name(code):
    """Return the human-readable name for a color code (code itself if unknown)."""
    if code in COLOR_NAMES:
        return COLOR_NAMES[code]
    if code.isdigit():
        index = int(code) - 7  # codes beyond '6' fall back to the extra list
        if 0 <= index < len(EXTRA_COLOR_NAMES):
            return EXTRA_COLOR_NAMES[index]
    return code
def palette_menu():
    """Return a one-line description of the palette, e.g. '1=Red 2=Blue ...'."""
    return '  '.join(
        '{}={}'.format(code, color_name(code)) for code in valid_codes()
    )
def normalize_guess_text(text):
    """Normalize raw player input into a list of color codes.
    Accepts forms like '1234', '1 2 3 4' or '1,2,3,4'. Returns None if the
    text cannot be interpreted as a sequence of color codes. The length of
    the resulting sequence is validated separately by the UI.
    """
    cleaned = text.replace(',', '').replace(' ', '').strip()
    codes = valid_codes()
    if not cleaned:
        return None
    result = []
    for ch in cleaned:
        if ch in codes:
            result.append(ch)
        else:
            return None
    return result