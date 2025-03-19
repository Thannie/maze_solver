"""
Algorithms to test:
    - Always Right
    - DFS
    - A*
    - Multi-agent maze-solving (bidirectional search)
"""

# TODO: BiDi-Solver still has the previous start and end

import heapq


class GridDFSSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
    
    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc] == 1:
                neighbors.append((nr, nc))
        return neighbors

    def solve(self, start, end):
        stack = [(start, [start])]
        visited = set()
        while stack:
            pos, path = stack.pop()
            if pos == end:
                return path
            if pos in visited:
                continue
            visited.add(pos)
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return None


class GridAStarSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
    
    def heuristic(self, pos, end):
        r, c = pos
        er, ec = end
        return abs(r - er) + abs(c - ec)
    
    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc] == 1:
                neighbors.append((nr, nc))
        return neighbors

    def solve(self, start, end):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}
        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == end:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]
            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, end)
                    if not any(neighbor == item[1] for item in open_set):
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None
