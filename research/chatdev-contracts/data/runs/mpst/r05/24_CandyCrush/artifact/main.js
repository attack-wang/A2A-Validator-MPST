<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Candy Match Deluxe</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="game-wrapper">
    <header>
      <h1>Candy Match Deluxe</h1>
    </header>
    <div class="hud">
      <div class="hud-item score">Score <span id="score">0</span></div>
      <div class="hud-item moves">Moves <span id="moves">30</span></div>
      <div class="hud-item time">Time <span id="time">150</span></div>
      <div class="hud-item combo">Combo <span id="combo">x1</span></div>
    </div>
    <div class="time-bar"><div id="time-fill"></div></div>
    <div id="board" class="board"></div>
    <div class="footer">
      <button id="restart">Restart</button>
      <p class="hint">Swap adjacent candies...</p>
    </div>
    <div id="overlay" class="overlay hidden">...</div>
    <div id="banner" class="banner hidden"></div>
  </div>
  <script src="js/constants.js"></script>
  <script src="js/board.js"></script>
  <script src="js/ui.js"></script>
  <script src="js/game.js"></script>
  <script src="js/main.js"></script>
</body>
</html>