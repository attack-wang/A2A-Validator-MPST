/* Global tuning constants for Candy Match Deluxe. */
const BOARD_SIZE = 8;
const NUM_TYPES = 6;
const CANDY_TYPES = [
  { name: 'cherry',    className: 'candy-red' },
  { name: 'orange',    className: 'candy-orange' },
  { name: 'lemon',     className: 'candy-yellow' },
  { name: 'lime',      className: 'candy-green' },
  { name: 'blueberry', className: 'candy-blue' },
  { name: 'grape',     className: 'candy-purple' },
];
const SWAP_DURATION = 220;   // ms for swap animation
const CLEAR_DURATION = 320;  // ms for clear/pop animation
const FALL_DURATION = 300;   // ms for fall animation
const POINTS_PER_CANDY = 60;
const RUN_BONUS = 60;        // extra points per candy beyond 3 in a run
const INITIAL_MOVES = 30;
const INITIAL_TIME = 150;    // seconds
const COMBO_MESSAGES = { 2: 'Sweet!', 3: 'Tasty!', 4: 'Delicious!', 5: 'Divine!' };
/* Shared promise-based delay helper used by every animation. */
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}