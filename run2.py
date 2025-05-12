import sys
import collections
from itertools import permutations

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    return [list(line.strip()) for line in sys.stdin]


def solve(data):
    grid = data
    robots = []
    all_keys = set()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':
                robots.append((i, j))
            elif grid[i][j] in keys_char:
                all_keys.add(grid[i][j])

    total_keys = len(all_keys)
    if total_keys == 0:
        return 0

    key_to_bit = {key: 1 << idx for idx, key in enumerate(sorted(all_keys))}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    initial_state = (*tuple(robots), 0)
    visited = set()
    visited.add(initial_state[:-1])
    queue = collections.deque()
    queue.append((*initial_state, 0))

    while queue:
        pos1, pos2, pos3, pos4, keys, steps = queue.popleft()

        if bin(keys).count('1') == total_keys:
            return steps

        for robot_idx in range(4):
            robots_pos = [pos1, pos2, pos3, pos4]
            x, y = robots_pos[robot_idx]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    cell = grid[nx][ny]

                    if cell == '#' or (cell in doors_char and not (keys & key_to_bit.get(cell.lower(), 0))):
                        continue

                    new_robots_pos = robots_pos.copy()
                    new_robots_pos[robot_idx] = (nx, ny)
                    new_pos1, new_pos2, new_pos3, new_pos4 = new_robots_pos

                    new_keys = keys
                    if cell in key_to_bit and not (keys & key_to_bit[cell]):
                        new_keys = keys | key_to_bit[cell]

                    state_without_steps = (new_pos1, new_pos2, new_pos3, new_pos4, new_keys)

                    if state_without_steps not in visited:
                        visited.add(state_without_steps)
                        queue.append((*state_without_steps, steps + 1))

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
    
