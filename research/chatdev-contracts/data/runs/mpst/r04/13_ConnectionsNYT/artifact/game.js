/**
 * game.js — core game logic and DOM wiring for Word Weave.
 */
(function () {
  'use strict';
  const LEVEL_COLORS = ['yellow', 'green', 'blue', 'purple'];
  const LEVEL_EMOJI = ['🟨', '🟩', '🟦', '🟪'];
  const MAX_MISTAKES = 4;
  const SELECTION_SIZE = 4;
  const els = { ... };
  class Game {
    constructor(puzzle, puzzleNumber, dateKey) {
      this.puzzle = puzzle;
      this.puzzleNumber = puzzleNumber;
      this.dateKey = dateKey;
      this.storageKey = 'wordweave-' + dateKey;
      this.wordToCategory = new Map();
      puzzle.categories.forEach((cat, ci) => {
        cat.words.forEach(w => this.wordToCategory.set(w, ci));
      });
      this.allWords = puzzle.categories.flatMap(c => c.words);
      this.state = this.loadState() || this.freshState();
      this.animating = false;
      this.timerId = null;
    }
    freshState() {
      return {
        order: shuffleArray(this.allWords.slice()),
        selected: [],
        solved: [],        // category indices in solve order
        mistakes: 0,
        history: [],       // arrays of category indices per guess
        finished: false,
        won: false
      };
    }
    loadState() {
      try {
        const raw = localStorage.getItem(this.storageKey);
        if (!raw) return null;
        const s = JSON.parse(raw);
        // validate
        if (!Array.isArray(s.order) || s.order.length !== 16) return null;
        return s;
      } catch (e) { return null; }
    }
    saveState() {
      try { localStorage.setItem(this.storageKey, JSON.stringify(this.state)); } catch (e) {}
    }
    remainingWords() {
      const solvedWords = new Set();
      this.state.solved.forEach(ci => this.puzzle.categories[ci].words.forEach(w => solvedWords.add(w)));
      return this.state.order.filter(w => !solvedWords.has(w));
    }
    start() {
      renderDateLabel...
      this.render();
      bind buttons...
      start countdown...
      if finished → openModal(won) maybe not auto-open; show a "show results" button? Simpler: if finished, auto-open modal once. I'll auto-open.
    }
    ...
  }
})();