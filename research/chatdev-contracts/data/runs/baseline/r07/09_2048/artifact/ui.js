.tile {
  position: absolute;
  width: var(--cell);
  height: var(--cell);
  transform: translate(calc(var(--x) * (var(--cell) + var(--gap))), calc(var(--y) * (var(--cell) + var(--gap))));
  transition: transform 0.12s ease-in-out;
}