/**
 * puzzles.js
 * Puzzle database and daily-puzzle selection logic.
 */
const PUZZLE_EPOCH = new Date(2024, 0, 1); // Jan 1 2024 — puzzle #0 reference date
const PUZZLES = [
  {
    categories: [
      { name: "CITRUS FRUITS", level: 0, words: ["LEMON", "CITRON", "POMELO", "KUMQUAT"] },
      { name: "SHADES OF PINK", level: 1, words: ["ROSE", "SALMON", "CORAL", "FUCHSIA"] },
      { name: "SEA CREATURES", level: 2, words: ["ANEMONE", "STARFISH", "JELLYFISH", "SEAHORSE"] },
      { name: "___ FISH", level: 3, words: ["CAT", "SWORD", "PARROT", "CLOWN"] },
    ],
  },
  ...
];
function getDayNumber() { ... }
function getDailyPuzzle() { ... }
function formatPuzzleDate(date) { ... }