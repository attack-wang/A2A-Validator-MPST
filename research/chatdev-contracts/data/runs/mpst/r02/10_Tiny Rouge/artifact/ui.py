generate_level(level):
1. grid = all walls (80x80)
2. Room-based generation:
   - Try to place N random rooms (rectangular, random size 5-11), non-overlapping (with 1-tile margin)
   - Connect room centers sequentially with L-shaped corridors
   - Also add a few extra random connections for loops
3. Start position: center of room 0 (or random floor)
4. Door: center of the farthest room from start (BFS distance) — ensures distance
5. Validate: BFS from start → door on floor tiles. If fail (shouldn't with corridor connection, but just in case), carve direct L-corridor between start and door.
6. Place chests: K chests on random floor tiles (not start, not door)
7. Place monsters: M monsters on random floor tiles (not start, not door, not on chest)
   - Monster stats scale with level
8. Return level data