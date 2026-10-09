/**
 * main.js — entry point.
 * Instantiates the Strands game once the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', () => {
  window.game = new StrandsGame(PUZZLES);
});