import heapq

# Define the goal state
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  # 0 is the blank tile

# Heuristic: Misplaced Tiles
def misplaced_tiles(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                count += 1
    return count

# Find the position of the blank (0)
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate possible moves from current state
def get_neighbors(state):
    neighbors = []
    x, y = find_blank(state)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors

# Check if two states are the same
def states_equal(s1, s2):
    return all(s1[i][j] == s2[i][j] for i in range(3) for j in range(3))

# A* Search
def a_star(start_state):
    pq = []
    heapq.heappush(pq, (misplaced_tiles(start_state), 0, start_state, []))
    visited = []

    while pq:
        f, g, state, path = heapq.heappop(pq)

        if states_equal(state, goal_state):
            return path + [state]

        visited.append(state)

        for neighbor in get_neighbors(state):
            if not any(states_equal(neighbor, v) for v in visited):
                h = misplaced_tiles(neighbor)
                heapq.heappush(pq, (g + 1 + h, g + 1, neighbor, path + [state]))

    return None

# Print state nicely
def print_state(state):
    for row in state:
        print(' '.join(str(cell) if cell != 0 else ' ' for cell in row))
    print()

# Example usage
if __name__ == "__main__":
    start = [[1, 2, 3],
             [4, 0, 6],
             [7, 5, 8]]

    print("🔵 Start State:")
    print_state(start)

    print("✅ Goal State:")
    print_state(goal_state)

    solution = a_star(start)

    if solution:
        print("🎯 Solution found in", len(solution) - 1, "moves.")
        for step, state in enumerate(solution):
            print(f"Step {step}:")
            print_state(state)
    else:
        print("❌ No solution found.")
