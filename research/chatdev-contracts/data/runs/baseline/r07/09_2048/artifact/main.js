/**
 * main.js
 * Entry point: wires the Game engine to the UIManager, binds keyboard
 * and button events, and drives the move -> render -> game-over loop.
 */
'use strict';
document.addEventListener('DOMContentLoaded', () => {
  const game = new Game(4);
  const ui = new UIManager(
    document.getElementById('game-board'),
    document.getElementById('score'),
    document.getElementById('best'),
    document.getElementById('highest'),
    document.getElementById('overlay'),
    document.getElementById('overlay-title'),
    document.getElementById('overlay-text'),
    document.getElementById('overlay-btn'),
    document.getElementById('new-game')
  );
  ui.init();          // build background cells
  ui.render(game, null);
  const KEY_MAP = {
    ArrowUp: 'up',
    ArrowDown: 'down',
    ArrowLeft: 'left',
    ArrowRight: 'right',
    w: 'up', s: 'down', a: 'left', d: 'right',
    W: 'up', S: 'down', A: 'left', D: 'right'
  };
  function handleMove(direction) {
    if (game.gameOver) return;
    const result = game.move(direction);   // move() spawns tile + checks game over internally
    if (!result) return;                   // nothing changed -> no render
    ui.render(game, result);
    if (game.won && !game.keepPlaying) {
      ui.showWin();
    } else if (game.gameOver) {
      ui.showGameOver();
    }
  }
  document.addEventListener('keydown', (event) => {
    if (event.key in KEY_MAP) {
      event.preventDefault();
      handleMove(KEY_MAP[event.key]);
    }
  });
  // New game button(s)
  document.getElementById('new-game').addEventListener('click', newGame);
  ui.overlayBtn.addEventListener('click', () => {
    if (game.gameOver) newGame();
    else { game.keepPlaying = true; ui.hideOverlay(); }
  });
  function newGame() {
    game.reset();
    ui.clearTiles();
    ui.render(game, null);
    ui.hideOverlay();
  }
});