'''
terminal_colors.py
Minimal ANSI escape-code helpers used to colorize palette labels and
feedback pegs in the terminal. All helpers degrade gracefully: an empty
ansi code returns the text unchanged.
'''
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
PEG_STYLES = {
    "exact": "\033[91m",    # bright red  (black pegs: right symbol, right slot)
    "partial": "\033[93m",  # bright yellow (white pegs: right symbol, wrong slot)
    "empty": "\033[90m",    # grey (unused pegs)
}
def colorize(text, ansi_code):
    """Wrap *text* in the given ANSI colour code (reset included)."""
    if not ansi_code:
        return text
    return f"{ansi_code}{text}{RESET}"
def style_peg(symbol, kind):
    """Return *symbol* coloured according to its peg kind."""
    return colorize(symbol, PEG_STYLES.get(kind, ""))