import heapq
import copy

class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return self.board == other.board


def misplaced_tiles(board, goal):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0 and board[i][j] != goal[i][j]:
                misplaced += 1
    return misplaced


def manhattan_distance(board, goal):
    dist = 0
    goal_pos = {}
    for i in range(3):
        for j in range(3):
            goal_pos[goal[i][j]] = (i, j)
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val != 0:
                gi, gj = goal_pos[val]
                dist += abs(i - gi) + abs(j - gj)
    return dist


def get_neighbors(state):
    moves = []
    board = state.board
    i, j = [(ix, iy) for ix, row in enumerate(board) for iy, v in enumerate(row) if v == 0][0]
    directions = {"Up": (-1,0), "Down": (1,0), "Left": (0,-1), "Right": (0,1)}
    for move, (di, dj) in directions.items():
        ni, nj = i+di, j+dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_board = copy.deepcopy(board)
            new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
            moves.append((move, new_board))
    return moves


def reconstruct_path(state):
    path = []
    while state.parent is not None:
        path.append((state.move, state.board))
        state = state.parent
    path.reverse()
    return path


def astar(start_board, goal_board, heuristic="manhattan"):
    if heuristic == "misplaced":
        h_func = misplaced_tiles
    else:
        h_func = manhattan_distance
    start_h = h_func(start_board, goal_board)
    start_state = PuzzleState(start_board, None, "", 0, start_h)
    frontier = []
    heapq.heappush(frontier, start_state)
    explored = set()
    while frontier:
        state = heapq.heappop(frontier)
        if state.board == goal_board:
            return reconstruct_path(state), state.g
        explored.add(hash(state))
        for move, board in get_neighbors(state):
            g = state.g + 1
            h = h_func(board, goal_board)
            neighbor = PuzzleState(board, state, move, g, h)
            if hash(neighbor) not in explored:
                heapq.heappush(frontier, neighbor)
    return None, None


def print_board(board):
    for row in board:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


if __name__ == "__main__":
    print("Enter the START state (3x3 grid, use 0 for blank):")
    start = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        start.append(row)

    print("\nEnter the GOAL state (3x3 grid, use 0 for blank):")
    goal = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        goal.append(row)

    print("\nInitial State:")
    print_board(start)
    print("Goal State:")
    print_board(goal)

    print("\n=== Solving with Misplaced Tiles Heuristic ===")
    path, cost = astar(start, goal, heuristic="misplaced")
    if path:
        print(f"Steps taken: {cost}")
        for move, board in path:
            print(f"Move: {move}")
            print_board(board)

    print("\n=== Solving with Manhattan Distance Heuristic ===")
    path, cost = astar(start, goal, heuristic="manhattan")
    if path:
        print(f"Steps taken: {cost}")
        for move, board in path:
            print(f"Move: {move}")
            print_board(board)
