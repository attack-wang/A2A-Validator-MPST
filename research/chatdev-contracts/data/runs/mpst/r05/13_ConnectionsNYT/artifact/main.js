/**
 * main.js
 * -------
 * Game logic for the daily 4x4 word-grouping puzzle ("Word Connections").
 *
 * The player must partition 16 words into 4 hidden categories of 4 words
 * each. Correct groups are removed from the board and revealed with a
 * color-coded difficulty banner (yellow, green, blue, purple). Wrong guesses
 * cost one of four allowed mistakes. A deterministic daily puzzle is chosen
 * from the PUZZLES bank so every player sees the same puzzle each day.
 */
"use strict";
// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------
/** Maximum wrong guesses before the game is lost. */
const MAX_MISTAKES = 4;
/** Number of words in a group (and the grid's row/column count). */
const GROUP_SIZE = 4;
/** Milliseconds in one day, used for the daily puzzle rotation. */
const MS_PER_DAY = 24 * 60 * 60 * 1000;
/** Maps category difficulty (0-3) to its CSS color class. */
const DIFFICULTY_CLASS = ["yellow", "green", "blue", "purple"];
/** Feedback messages shown to the player. */
const MESSAGES = {
  SELECT_FOUR: "Select four words to make a group",
  NOT_QUITE: "Not quite!",
  ONE_AWAY: "One away...!",
  WIN: "You did it! Perfect grouping.",
  LOSE: "Better luck next time!"
};
// ---------------------------------------------------------------------------
// Game state
// ---------------------------------------------------------------------------
let currentPuzzle = null;      // Deep copy of today's puzzle (PUZZLES is never mutated)
let remainingWords = [];       // Words still visible on the board
let selectedWords = [];        // Currently selected words (max GROUP_SIZE)
let mistakesRemaining = MAX_MISTAKES;
let solvedNames = new Set();   // Names of categories already solved
let isGameOver = false;        // True once the game is won or lost
// ---------------------------------------------------------------------------
// Daily puzzle selection
// ---------------------------------------------------------------------------
/**
 * Returns a stable day counter: the number of whole days elapsed since
 * 1970-01-01 UTC. Using UTC guarantees every player worldwide receives the
 * same puzzle on the same calendar day.
 * @returns {number} Whole days since the Unix epoch (UTC).
 */
function getDayNumber() {
  const now = new Date();
  const utcMidnight = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Math.floor(utcMidnight / MS_PER_DAY);
}
/**
 * Deterministically maps today's day number onto the puzzle bank so the
 * puzzle rotates day by day and repeats once the bank is exhausted.
 * @returns {number} Index into the PUZZLES array for today.
 */
function getDailyPuzzleIndex() {
  return getDayNumber() % PUZZLES.length;
}
/**
 * Returns a deep copy of today's puzzle so the shared PUZZLES bank is never
 * mutated during play.
 * @returns {Object} Today's puzzle object with its four categories.
 */
function getDailyPuzzle() {
  return JSON.parse(JSON.stringify(PUZZLES[getDailyPuzzleIndex()]));
}
// ---------------------------------------------------------------------------
// Game lifecycle
// ---------------------------------------------------------------------------
/**
 * Resets all state, loads today's puzzle, shuffles the 16 words and renders
 * the initial board.
 */
function startNewGame() {
  currentPuzzle = getDailyPuzzle();
  remainingWords = currentPuzzle.categories.flatMap((category) => category.words);
  selectedWords = [];
  mistakesRemaining = MAX_MISTAKES;
  solvedNames = new Set();
  isGameOver = false;
  document.getElementById("solved-groups").innerHTML = "";
  document.getElementById("banner").classList.add("hidden");
  document.getElementById("puzzle-number").textContent =
    "Puzzle #" + getDailyPuzzleIndex() + " \u2022 " + getTodayLabel();
  updateMistakesDots();
  showMessage("");
  shuffleWords(); // shuffles and renders the grid
  updateButtons();
}
/**
 * Returns a human-readable label for today's date, e.g. "Jan 15, 2025".
 * @returns {string} Formatted date string.
 */
function getTodayLabel() {
  return new Date().toLocaleDateString(undefined, {
    year: "numeric", month: "short", day: "numeric"
  });
}
// ---------------------------------------------------------------------------
// Board rendering
// ---------------------------------------------------------------------------
/**
 * Renders the 4x4 grid from remainingWords. Tiles for currently selected
 * words get the "selected" class.
 */
function renderGrid() {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  remainingWords.forEach((word) => {
    const tile = createTile(word);
    if (selectedWords.includes(word)) {
      tile.classList.add("selected");
    }
    grid.appendChild(tile);
  });
}
/**
 * Creates one clickable tile button for a word.
 * @param {string} word - The word displayed on the tile.
 * @returns {HTMLButtonElement} The tile element.
 */
function createTile(word) {
  const tile = document.createElement("button");
  tile.type = "button";
  tile.className = "tile";
  tile.textContent = word;
  tile.dataset.word = word;
  tile.addEventListener("click", () => toggleWord(word));
  return tile;
}
/**
 * Shuffles remainingWords in place with the Fisher–Yates algorithm and
 * re-renders the grid. The current selection is preserved (matched by value).
 */
function shuffleWords() {
  if (isGameOver) return;
  for (let i = remainingWords.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [remainingWords[i], remainingWords[j]] = [remainingWords[j], remainingWords[i]];
  }
  renderGrid();
}
// ---------------------------------------------------------------------------
// Selection and guessing
// ---------------------------------------------------------------------------
/**
 * Toggles a word in or out of the selection. A maximum of GROUP_SIZE words
 * can be selected at once; extra clicks are ignored.
 * @param {string} word - The word whose tile was clicked.
 */
function toggleWord(word) {
  if (isGameOver) return;
  const index = selectedWords.indexOf(word);
  if (index !== -1) {
    selectedWords.splice(index, 1); // Deselect
  } else if (selectedWords.length < GROUP_SIZE) {
    selectedWords.push(word);       // Select
  } else {
    return; // Already four selected — ignore the extra click
  }
  renderGrid();
  updateButtons();
}
/**
 * Clears the current selection and re-renders the grid.
 */
function clearSelection() {
  if (isGameOver) return;
  selectedWords = [];
  renderGrid();
  updateButtons();
}
/**
 * Validates the current selection against the hidden categories.
 * A correct guess solves the matching category; a wrong guess costs a
 * mistake and triggers immediate feedback.
 */
function submitGuess() {
  if (isGameOver || selectedWords.length !== GROUP_SIZE) return;
  const guess = selectedWords.slice();
  const match = currentPuzzle.categories.find(
    (category) => !solvedNames.has(category.name) && isCorrectGroup(guess, category)
  );
  if (match) {
    solveCategory(match);
  } else {
    handleWrongGuess(guess);
  }
  selectedWords = [];
  renderGrid();
  updateButtons();
}
/**
 * Checks whether the selected words exactly match a category's word set.
 * @param {string[]} selected - The four guessed words.
 * @param {Object} category - The category to compare against.
 * @returns {boolean} True if the guess matches the category exactly.
 */
function isCorrectGroup(selected, category) {
  const guessKey = selected.slice().sort().join("|");
  const answerKey = category.words.slice().sort().join("|");
  return guessKey === answerKey;
}
/**
 * Handles a wrong guess: consumes a mistake, shakes the board, shows
 * immediate feedback ("One away...!" when exactly three guessed words share
 * one category) and ends the game if no mistakes remain.
 * @param {string[]} guess - The four guessed words.
 */
function handleWrongGuess(guess) {
  mistakesRemaining--;
  updateMistakesDots();
  const grid = document.getElementById("grid");
  grid.classList.add("shake");
  setTimeout(() => grid.classList.remove("shake"), 500);
  const bestOverlap = getBestCategoryOverlap(guess);
  showMessage(bestOverlap === GROUP_SIZE - 1 ? MESSAGES.ONE_AWAY : MESSAGES.NOT_QUITE);
  if (mistakesRemaining <= 0) {
    isGameOver = true;
    setTimeout(showLoss, 700);
  }
}
/**
 * Computes the highest overlap between the guessed words and any unsolved
 * category, used to decide whether the guess was "one away".
 * @param {string[]} guess - The four guessed words.
 * @returns {number} Largest number of guessed words belonging to one category.
 */
function getBestCategoryOverlap(guess) {
  let best = 0;
  currentPuzzle.categories.forEach((category) => {
    if (solvedNames.has(category.name)) return; // Skip already-solved categories
    const overlap = category.words.filter((word) => guess.includes(word)).length;
    if (overlap > best) best = overlap;
  });
  return best;
}
// ---------------------------------------------------------------------------
// Solving, revealing and game end
// ---------------------------------------------------------------------------
/**
 * Removes a solved group from the board and appends its reveal banner,
 * color-coded by the category's difficulty.
 * @param {Object} category - The solved category.
 */
function solveCategory(category) {
  solvedNames.add(category.name);
  remainingWords = remainingWords.filter((word) => !category.words.includes(word));
  appendRevealBanner(category);
  showMessage("");
  if (solvedNames.size === currentPuzzle.categories.length) {
    isGameOver = true;
    setTimeout(showWin, 400);
  }
}
/**
 * Builds and appends a reveal banner for a category.
 * @param {Object} category - The category to reveal.
 */
function appendRevealBanner(category) {
  const banner = document.createElement("div");
  banner.className = "reveal " + DIFFICULTY_CLASS[category.difficulty];
  const name = document.createElement("span");
  name.className = "reveal-name";
  name.textContent = category.name;
  const words = document.createElement("span");
  words.className = "reveal-words";
  words.textContent = category.words.join(", ");
  banner.appendChild(name);
  banner.appendChild(words);
  document.getElementById("solved-groups").appendChild(banner);
}
/**
 * Reveals every unsolved category (used when the player runs out of
 * mistakes), then shows the loss banner.
 */
function revealSolution() {
  currentPuzzle.categories.forEach((category) => {
    if (!solvedNames.has(category.name)) {
      appendRevealBanner(category);
    }
  });
  remainingWords = [];
  renderGrid();
}
/**
 * Shows the win banner.
 */
function showWin() {
  showMessage("");
  showBanner(MESSAGES.WIN);
}
/**
 * Reveals the remaining categories and shows the loss banner.
 */
function showLoss() {
  revealSolution();
  showBanner(MESSAGES.LOSE);
}
/**
 * Displays the end-of-game banner with a "Play again" button.
 * @param {string} text - The banner message.
 */
function showBanner(text) {
  document.getElementById("banner-text").textContent = text;
  document.getElementById("banner").classList.remove("hidden");
  updateButtons();
}
// ---------------------------------------------------------------------------
// UI helpers
// ---------------------------------------------------------------------------
/**
 * Renders the mistake dots: filled dots for remaining mistakes, empty for
 * used ones.
 */
function updateMistakesDots() {
  const container = document.getElementById("mistakes-dots");
  container.innerHTML = "";
  for (let i = 0; i < MAX_MISTAKES; i++) {
    const dot = document.createElement("span");
    dot.className = "dot" + (i < mistakesRemaining ? " filled" : "");
    container.appendChild(dot);
  }
}
/**
 * Shows a transient feedback message under the grid.
 * @param {string} text - The message to display (empty string hides it).
 */
function showMessage(text) {
  const element = document.getElementById("message");
  element.textContent = text;
  element.classList.toggle("visible", text !== "");
}
/**
 * Enables/disables the control buttons according to the game state.
 */
function updateButtons() {
  document.getElementById("submit-btn").disabled =
    isGameOver || selectedWords.length !== GROUP_SIZE;
  document.getElementById("shuffle-btn").disabled = isGameOver;
  document.getElementById("deselect-btn").disabled =
    isGameOver || selectedWords.length === 0;
  document.getElementById("play-again-btn").disabled = false;
}
// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------
/**
 * Wires up button handlers and starts a new game once the DOM is ready.
 */
function init() {
  document.getElementById("shuffle-btn").addEventListener("click", shuffleWords);
  document.getElementById("deselect-btn").addEventListener("click", clearSelection);
  document.getElementById("submit-btn").addEventListener("click", submitGuess);
  document.getElementById("play-again-btn").addEventListener("click", startNewGame);
  startNewGame();
}
document.addEventListener("DOMContentLoaded", init);