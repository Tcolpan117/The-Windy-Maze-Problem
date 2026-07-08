import heapq

ROWS = 5
COLS = 6

start = (0, 1)
goal = (2, 3)

obstacles = {
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 4),
    (3, 1)
}

# Move order:
# west, north, east, south
# Labels are direction label, change in position, and cost of move
moves = [
    ("W", (0, -1), 1),
    ("N", (-1, 0), 2),
    ("E", (0, 1), 3),
    ("S", (1, 0), 2)
]


def heuristic(position):
    row, col = position
    goal_row, goal_col = goal

    vertical_cost = abs(goal_row - row) * 2

    if goal_col > col:
        horizontal_cost = (goal_col - col) * 3
    else:
        horizontal_cost = (col - goal_col) * 1

    return vertical_cost + horizontal_cost


def is_valid(position):
    row, col = position

    if row < 0 or row >= ROWS:
        return False

    if col < 0 or col >= COLS:
        return False

    if position in obstacles:
        return False

    return True


def print_maze(labels):
    for row in range(ROWS):
        line = []

        for col in range(COLS):
            position = (row, col)

            if position in obstacles:
                line.append("##")
            elif position == goal:
                line.append("GG")
            elif position in labels:
                line.append(f"{labels[position]:02d}")
            else:
                line.append("[]")

        print(" ".join(line))


def a_star_search():
    frontier = []
    explored = set()

    labels = {start: 0}
    goal_cost = {start: 0}

    next_label = 1

    # heap stores: f, label, position
    heapq.heappush(frontier, (heuristic(start), 0, start))

    search_steps = []
    
    print('\n')
    print("Searching...")

    while frontier:
        f, label, current = heapq.heappop(frontier)

        if current in explored:
            continue

        explored.add(current)

        search_steps.append({
            "label": label,
            "position": current,
            "g": goal_cost[current],
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

            if not is_valid(new_pos) or new_pos in explored or new_pos in labels:
                continue


            labels[new_pos] = next_label
            goal_cost[new_pos] = goal_cost[current] + move_cost

            new_f = goal_cost[new_pos] + heuristic(new_pos)

            heapq.heappush(frontier, (new_f, next_label, new_pos))

            next_label += 1

        print('\n')
        print_maze(labels)
        print(
            f"Label {search_steps[-1]['label']:02d}: "
            f"Position {search_steps[-1]['position']}, "
            f"g={search_steps[-1]['g']}, "
            f"h={search_steps[-1]['h']}, "
            f"f={search_steps[-1]['f']}"
        )


a_star_search()