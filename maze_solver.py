"""
Algorithms to test:
    - Always Right
    - DFS
    - A*
    - Multi-agent maze-solving (bidirectional search)
"""

# TODO: BiDi-Solver still has the previous start and end

import heapq


class AlwaysRightSolver:
    """
    Implements the "Always Right" (wall-follower) maze solving algorithm.
    
    The algorithm always attempts to turn right relative to its current direction,
    then straight, left, and finally back if necessary.
    """
    def __init__(self, maze_generator):
        self.maze_generator = maze_generator
        self.rows = maze_generator.rows
        self.cols = maze_generator.cols

    def can_move(self, cell, direction):
        """
        Checks if movement from a cell in a given direction is possible.
        
        Direction indices: 0: North, 1: East, 2: South, 3: West.
        """
        if direction == 0:
            return not cell.walls['top']
        elif direction == 1:
            return not cell.walls['right']
        elif direction == 2:
            return not cell.walls['bottom']
        elif direction == 3:
            return not cell.walls['left']

    def move(self, cell, direction):
        """
        Returns the neighboring cell in the given direction.
        """
        row, col = cell.row, cell.col
        if direction == 0:
            return self.maze_generator.get_cell(row - 1, col)
        elif direction == 1:
            return self.maze_generator.get_cell(row, col + 1)
        elif direction == 2:
            return self.maze_generator.get_cell(row + 1, col)
        elif direction == 3:
            return self.maze_generator.get_cell(row, col - 1)

    def solve(self, start, end):
        """
        Solves the maze using the "Always Right" algorithm.
        
        Parameters:
            start (MazeCell): The starting cell.
            end (MazeCell): The goal cell.
        
        Returns:
            A list of MazeCell objects representing the path, or None if no path is found.
        """
        current = start
        direction = 1  # Start facing East.
        path = [current]
        max_iterations = self.rows * self.cols * 10  # Safety to prevent infinite loops.
        iterations = 0

        while current != end and iterations < max_iterations:
            iterations += 1
            moved = False
            # Try directions in the order: right, straight, left, back.
            for delta in [1, 0, -1, 2]:
                new_direction = (direction + delta) % 4
                if self.can_move(current, new_direction):
                    next_cell = self.move(current, new_direction)
                    if next_cell is not None:
                        direction = new_direction
                        current = next_cell
                        path.append(current)
                        moved = True
                        break
            if not moved:
                break

        return path if current == end else None


class DFSSolver:
    """
    Implements a depth-first search maze solving algorithm.
    
    This iterative DFS returns a path from the start cell to the goal cell.
    """
    def __init__(self, maze_generator):
        self.maze_generator = maze_generator
        self.rows = maze_generator.rows
        self.cols = maze_generator.cols

    def get_neighbors(self, cell):
        """
        Retrieves all reachable neighboring cells (i.e. where walls are absent).
        """
        neighbors = []
        row, col = cell.row, cell.col
        if not cell.walls['top']:
            neighbor = self.maze_generator.get_cell(row - 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['right']:
            neighbor = self.maze_generator.get_cell(row, col + 1)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['bottom']:
            neighbor = self.maze_generator.get_cell(row + 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['left']:
            neighbor = self.maze_generator.get_cell(row, col - 1)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def solve(self, start=None, end=None):
        """
        Solves the maze using DFS.
        
        Returns:
            A list of MazeCell objects representing the solution path.
        """
        if start is None:
            start = self.maze_generator.get_cell(0, 0)
        if end is None:
            end = self.maze_generator.get_cell(self.rows - 1, self.cols - 1)
        stack = [(start, [start])]
        visited = set()

        while stack:
            cell, path = stack.pop()
            if cell == end:
                return path
            visited.add((cell.row, cell.col))
            for neighbor in self.get_neighbors(cell):
                if (neighbor.row, neighbor.col) not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return None


class AStarSolver:
    """
    Implements the A* maze solving algorithm using Manhattan distance as the heuristic.
    """
    def __init__(self, maze_generator):
        self.maze_generator = maze_generator
        self.rows = maze_generator.rows
        self.cols = maze_generator.cols

    def heuristic(self, cell, goal):
        """
        Computes the Manhattan distance heuristic.
        """
        return abs(cell.row - goal.row) + abs(cell.col - goal.col)

    def get_neighbors(self, cell):
        """
        Retrieves all reachable neighboring cells.
        """
        neighbors = []
        row, col = cell.row, cell.col
        if not cell.walls['top']:
            neighbor = self.maze_generator.get_cell(row - 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['right']:
            neighbor = self.maze_generator.get_cell(row, col + 1)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['bottom']:
            neighbor = self.maze_generator.get_cell(row + 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['left']:
            neighbor = self.maze_generator.get_cell(row, col - 1)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def solve(self, start=None, end=None):
        """
        Solves the maze using the A* algorithm.
        
        Returns:
            A list of MazeCell objects representing the solution path.
        """
        if start is None:
            start = self.maze_generator.get_cell(0, 0)
        if end is None:
            end = self.maze_generator.get_cell(self.rows - 1, self.cols - 1)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {(start.row, start.col): 0}
        f_score = {(start.row, start.col): self.heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == end:
                # Reconstruct path
                path = [current]
                while (current.row, current.col) in came_from:
                    current = came_from[(current.row, current.col)]
                    path.append(current)
                return path[::-1]
            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[(current.row, current.col)] + 1
                neighbor_key = (neighbor.row, neighbor.col)
                if tentative_g < g_score.get(neighbor_key, float('inf')):
                    came_from[neighbor_key] = current
                    g_score[neighbor_key] = tentative_g
                    f_score[neighbor_key] = tentative_g + self.heuristic(neighbor, end)
                    if not any(neighbor == item[1] for item in open_set):
                        heapq.heappush(open_set, (f_score[neighbor_key], neighbor))
        return None


class MultiAgentSolver:
    """
    Implements a bidirectional (multi-agent) maze solver.
    
    Two simultaneous breadth-first searches are run from the start and goal.
    The search terminates when the frontiers meet, and the full path is reconstructed.
    """
    def __init__(self, maze_generator):
        self.maze_generator = maze_generator
        self.rows = maze_generator.rows
        self.cols = maze_generator.cols

    def get_neighbors(self, cell):
        """
        Retrieves all reachable neighboring cells.
        """
        neighbors = []
        row, col = cell.row, cell.col
        if not cell.walls['top']:
            neighbor = self.maze_generator.get_cell(row - 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['right']:
            neighbor = self.maze_generator.get_cell(row, col + 1)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['bottom']:
            neighbor = self.maze_generator.get_cell(row + 1, col)
            if neighbor:
                neighbors.append(neighbor)
        if not cell.walls['left']:
            neighbor = self.maze_generator.get_cell(row, col - 1)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def solve(self):
        """
        Solves the maze using bidirectional search.
        
        Returns:
            A list of MazeCell objects representing the solution path, or None if not found.
        """
        start = self.maze_generator.get_cell(0, 0)
        goal = self.maze_generator.get_cell(self.rows - 1, self.cols - 1)
        frontier_start = [start]
        frontier_goal = [goal]
        came_from_start = {(start.row, start.col): None}
        came_from_goal = {(goal.row, goal.col): None}
        meeting_point = None

        while frontier_start and frontier_goal:
            new_frontier = []
            for cell in frontier_start:
                for neighbor in self.get_neighbors(cell):
                    key = (neighbor.row, neighbor.col)
                    if key not in came_from_start:
                        came_from_start[key] = cell
                        new_frontier.append(neighbor)
                        if key in came_from_goal:
                            meeting_point = neighbor
                            break
                if meeting_point:
                    break
            if meeting_point:
                break
            frontier_start = new_frontier

            new_frontier = []
            for cell in frontier_goal:
                for neighbor in self.get_neighbors(cell):
                    key = (neighbor.row, neighbor.col)
                    if key not in came_from_goal:
                        came_from_goal[key] = cell
                        new_frontier.append(neighbor)
                        if key in came_from_start:
                            meeting_point = neighbor
                            break
                if meeting_point:
                    break
            if meeting_point:
                break
            frontier_goal = new_frontier

        if not meeting_point:
            return None

        # Reconstruct path from start to meeting point.
        path_start = []
        cell = meeting_point
        while cell is not None:
            path_start.append(cell)
            cell = came_from_start.get((cell.row, cell.col))
        path_start = path_start[::-1]

        # Reconstruct path from meeting point to goal.
        path_goal = []
        cell = came_from_goal.get((meeting_point.row, meeting_point.col))
        while cell is not None:
            path_goal.append(cell)
            cell = came_from_goal.get((cell.row, cell.col))

        return path_start + path_goal
