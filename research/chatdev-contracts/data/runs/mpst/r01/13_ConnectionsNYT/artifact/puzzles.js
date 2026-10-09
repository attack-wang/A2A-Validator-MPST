/* puzzles.js — Puzzle data for WordWeave.
 * Each puzzle contains exactly four categories; each category has a name,
 * a difficulty (0 = yellow/easiest … 3 = purple/hardest) and exactly four words.
 * All 16 words within a puzzle are unique so that exactly one correct
 * solution exists, even though words may appear to fit multiple categories.
 */
const PUZZLES = [ ... 12 puzzles ... ];
/**
 * Dev-time integrity check ...
 */
function validatePuzzles() {
  const problems = [];
  PUZZLES.forEach((puzzle, index) => {
    if (!Array.isArray(puzzle.categories) || puzzle.categories.length !== 4) {
      problems.push(`Puzzle ${index}: must contain exactly 4 categories`);
      return;
    }
    const difficulties = new Set();
    const seen = new Set();
    puzzle.categories.forEach(cat => {
      if (!cat || typeof cat.name !== 'string' || !cat.name.trim()) problems.push(...);
      if (!Number.isInteger(cat.difficulty) || cat.difficulty < 0 || cat.difficulty > 3) problems.push(...);
      if (difficulties.has(cat.difficulty)) problems.push(`Puzzle ${index}: duplicate difficulty ${cat.difficulty}`);
      difficulties.add(cat.difficulty);
      if (!Array.isArray(cat.words) || cat.words.length !== 4) problems.push(...);
      cat.words.forEach(w => {
        if (typeof w !== 'string' || !w.trim()) problems.push(...);
        const key = w.trim().toUpperCase();
        if (seen.has(key)) problems.push(`Puzzle ${index}: duplicate word "${w}"`);
        seen.add(key);
      });
    });
  });
  if (problems.length) {
    console.error('Puzzle data integrity check failed:', problems);
    throw new Error('Puzzle data invalid: ' + problems.join('; '));
  }
  return true;
}