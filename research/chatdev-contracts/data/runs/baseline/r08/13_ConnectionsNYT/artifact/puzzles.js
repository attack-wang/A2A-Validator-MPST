/**
 * puzzles.js
 * Puzzle library and daily-puzzle selection logic for the word-grouping game.
 *
 * Puzzle invariants (enforced at load time by isValidPuzzle):
 *   - exactly 4 categories per puzzle
 *   - each category: exactly 4 words + a unique difficulty 0..3
 *     (0 = yellow, 1 = green, 2 = blue, 3 = purple)
 *   - all 16 words unique within a puzzle -> exactly one correct grouping,
 *     even though words may *appear* to fit multiple categories
 */
/** Reference date for daily numbering: Jan 1, 2024 counts as puzzle #0. */
const PUZZLE_EPOCH = new Date(2024, 0, 1);
/**
 * Master puzzle library.
 * NOTE: expand to 365+ entries so the daily rotation serves a different
 * puzzle every calendar day; until then it cycles through existing entries.
 */
const PUZZLES = [ ... multiple entries ... ];
/**
 * Returns the number of whole calendar days between PUZZLE_EPOCH and date.
 * Uses midnight-normalized timestamps and Math.round so DST transitions
 * cannot introduce off-by-one errors.
 */
function getDaysSinceEpoch(date) {
  const start = new Date(PUZZLE_EPOCH.getFullYear(), PUZZLE_EPOCH.getMonth(), PUZZLE_EPOCH.getDate()).getTime();
  const end = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime();
  const MS_PER_DAY = 24 * 60 * 60 * 1000;
  return Math.round((end - start) / MS_PER_DAY);
}
function getDailyPuzzleIndex(date) {
  if (!PUZZLES || PUZZLES.length === 0) {
    throw new Error("Puzzle library is empty.");
  }
  const days = getDaysSinceEpoch(date);
  // Double modulo guarantees a non-negative index even for pre-epoch dates.
  return ((days % PUZZLES.length) + PUZZLES.length) % PUZZLES.length;
}
function getDailyPuzzle(date) {
  const index = getDailyPuzzleIndex(date);
  // Deep copy so callers (e.g., shuffle logic) cannot mutate the shared library.
  return JSON.parse(JSON.stringify(PUZZLES[index]));
}
function getPuzzleNumber(date) {
  return getDaysSinceEpoch(date) + 1;
}
function isValidPuzzle(puzzle) { ... }
// Load-time validation
PUZZLES.forEach((p, i) => {
  if (!isValidPuzzle(p)) {
    throw new Error(`Invalid puzzle at index ${i}`);
  }
});