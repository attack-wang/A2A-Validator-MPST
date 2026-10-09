/**
 * puzzles.js
 * Puzzle data bank and daily puzzle selection logic.
 */
const PUZZLE_BANK = [
  {
    id: 1,
    groups: [
      { category: "KINDS OF BREAD", difficulty: 0, words: ["RYE", "SOURDOUGH", "BAGUETTE", "FOCACCIA"] },
      { category: "CARD GAMES", difficulty: 1, words: ["BRIDGE", "SOLITAIRE", "HEARTS", "SPADES"] },
      ...
    ]
  },
  ...
];
function getDaysSinceEpoch() { ... }
function getDailyPuzzleIndex() { ... }
function getDailyPuzzle() { ... }
function getPuzzleByIndex(i) { ... }