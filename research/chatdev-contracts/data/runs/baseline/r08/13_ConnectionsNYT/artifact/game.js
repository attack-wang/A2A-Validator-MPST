/**
 * game.js
 * Game logic: grid rendering, selection, guessing, shuffle, mistakes,
 * persistence, and daily reset for the word-grouping puzzle.
 */
(function () {
  "use strict";
  const MAX_MISTAKES = 4;
  const GROUP_SIZE = 4;
  const DIFFICULTY_COLORS = ["yellow", "green", "blue", "purple"];
  const STORAGE_KEY_PREFIX = "wordgrid-daily-";
  // DOM refs
  const gridEl = document.getElementById("grid");
  const solvedEl = document.getElementById("solved-groups");
  const messageEl = document.getElementById("message");
  const dotsEl = document.getElementById("mistake-dots");
  const submitBtn = document.getElementById("submit-btn");
  const shuffleBtn = document.getElementById("shuffle-btn");
  const deselectBtn = document.getElementById("deselect-btn");
  const gameOverEl = document.getElementById("game-over");
  ...
  // State
  let puzzle;
  let puzzleNumber;
  let tiles = [];          // remaining tiles: { word, categoryIndex, difficulty, element }
  let solved = [];         // solved category indices, in solve order
  let mistakes = 0;
  let selected = new Set(); // words currently selected
  let locked = false;       // input lock during animations / game over
  let status = "playing";   // "playing" | "won" | "lost"
  ...
})();