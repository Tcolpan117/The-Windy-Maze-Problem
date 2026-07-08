import heapq

# Maze setup
# [] = open square
# ## = obstacle
# 00 = start
# GG = goal

ROWS = 5
COLS = 6

start = (0, 1)
goal = (2, 3)

obstacles = {
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 4),
    (3, 1)
}

# Move order required by the assignment:
# west, north, east, south
moves = [
    ("W", (0, -1), 1),
    ("N", (-1, 0), 2),
    ("E", (0, 1), 3),
    ("S", (1, 0), 2)
]


def heuristic(pos):
    """
    Modified Manhattan distance using windy movement costs.
    West = 1
    North/South = 2
    East = 3
    """
    r, c = pos
    gr, gc = goal

    vertical_cost = abs(gr - r) * 2

    if gc > c:
        horizontal_cost = (gc - c) * 3
    else:
        horizontal_cost = (c - gc) * 1

    return vertical_cost + horizontal_cost


def is_valid(pos):
    r, c = pos

    if r < 0 or r >= ROWS:
        return False

    if c < 0 or c >= COLS:
        return False

    if pos in obstacles:
        return False

    return True


def a_star():
    frontier = []
    explored = set()

    labels = {start: 0}
    g_cost = {start: 0}

    next_label = 1

    # heap stores: f, label, position
    heapq.heappush(frontier, (heuristic(start), 0, start))

    search_steps = []

    while frontier:
        f, label, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        search_steps.append({
            "label": label,
            "position": current,
            "g": g_cost[current],
            "h": heuristic(current),
            "f": f
        })

        if current == goal:
            break

        for direction, change, move_cost in moves:
            new_pos = (
                current[0] + change[0],
                current[1] + change[1]
            )

            if not is_valid(new_pos):
                continue

            if new_pos in explored:
                continue

            if new_pos in labels:
                continue

            labels[new_pos] = next_label
            g_cost[new_pos] = g_cost[current] + move_cost

            new_f = g_cost[new_pos] + heuristic(new_pos)

            heapq.heappush(frontier, (new_f, next_label, new_pos))

            next_label += 1

    return labels, search_steps


def print_final_maze(labels):
    for r in range(ROWS):
        row = []

        for c in range(COLS):
            pos = (r, c)

            if pos in obstacles:
                row.append("##")
            elif pos == goal:
                row.append("GG")
            elif pos in labels:
                row.append(f"{labels[pos]:02d}")
            else:
                row.append("[]")

        print(" ".join(row))


labels, steps = a_star()

print("Search Steps:")
for step in steps:
    print(
        f"Label {step['label']:02d}: "
        f"Position {step['position']}, "
        f"g={step['g']}, "
        f"h={step['h']}, "
        f"f={step['f']}"
    )

print("\nFinal Maze:")
print_final_maze(labels)

#asdfghjk