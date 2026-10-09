const STORAGE_KEY_PREFIX = 'wordweave-state-';
function getStorageKey(dayNumber) { return `${STORAGE_KEY_PREFIX}${dayNumber}`; }
function loadSavedState(dayNumber) {
  try {
    const raw = localStorage.getItem(getStorageKey(dayNumber));
    return raw ? JSON.parse(raw) : null;
  } catch (e) { return null; }
}
function saveState(dayNumber, game) {
  try { localStorage.setItem(getStorageKey(dayNumber), JSON.stringify(game.serialize())); } catch(e) {}
}
document.addEventListener('DOMContentLoaded', () => {
  validatePuzzles(); // integrity check
  const dayNumber = getDayNumber();
  const puzzle = getDailyPuzzle();
  let game = Game.deserialize(loadSavedState(dayNumber), puzzle, dayNumber) || new Game(puzzle, dayNumber);
  const ui = new UI(game);
  ui.init();
  game.addChangeListener(g => saveState(dayNumber, g));
  // if restored finished game, show results
  if (game.isGameOver()) { ui.showGameOver(); }
});