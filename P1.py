#CIS-479 Project 1 (Group 2)
#Windy Maze Problem

#Members:
#Taylan Colpan
#Gustavo Abreu

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

# Direction label, change in position, and cost of move
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

    # Mahattan distance
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
    # 3:
    # The frontier is implemented as a priority queue using Python's heapq module.
    # The explored set is implemented as a Python set, which is hash-table based.
    # This allows the program to quickly check if a node has already been explored.
    frontier = []
    explored = set()

    labels = {start: 0}
    goal_cost = {start: 0}

    next_label = 1
    insert_order = 1
    final_path_cost = None

    # The priority queue removes the node with the smallest f(n) value first.
    heapq.heappush(frontier, (heuristic(start), 0, start))

    search_steps = []

    print("\nSearching...")

    while frontier:


        #6:
        # Pick and remove the node with the smallest f(n) value from the frontier.
        # This is the key step of A* search.
        f, order, current = heapq.heappop(frontier)

        if current in explored:
            continue

        # Label the square only when it is actually explored
        if current not in labels:
            labels[current] = next_label
            next_label += 1

        explored.add(current)

        current_label = labels[current]

        search_steps.append({
            "label": current_label,
            "position": current,
            "g": goal_cost[current],
            "h": heuristic(current),
            "f": goal_cost[current] + heuristic(current)
        })

        print("\n")
        print_maze(labels)
        print(
            f"Label {current_label:02d}: "
            f"Position {current}, "
            f"g={goal_cost[current]}, "
            f"h={heuristic(current)}, "
            f"f={goal_cost[current] + heuristic(current)}"
        )

        if current == goal:
            final_path_cost = goal_cost[current]
            break

        # 5:
        # This loop expands the current node by checking its child nodes,
        # also called leaves, in the required order:
        # west, north, east, and south.
        for direction, change, move_cost in moves:
            new_pos = (
                current[0] + change[0],
                current[1] + change[1]
            )

            if not is_valid(new_pos):
                continue

            if new_pos in explored:
                continue

            # 4:
            # Calculate g(n), which is the total path cost from the start node
            # to this child node.
            new_goal_cost = goal_cost[current] + move_cost

            if new_pos not in goal_cost or new_goal_cost < goal_cost[new_pos]:
                goal_cost[new_pos] = new_goal_cost

                # 4 Cont.:
                # Calculate f(n) = g(n) + h(n).
                # g(n) is the path cost so far.
                # h(n) is the windy Manhattan heuristic estimate to the goal.
                new_f = new_goal_cost + heuristic(new_pos)

                # Adding the frontier
                heapq.heappush(frontier, (new_f, insert_order, new_pos))
                insert_order += 1

    print("\nFinal Maze:")
    print_maze(labels)

    print(f"\nFinal Path Cost: {final_path_cost}")

a_star_search()