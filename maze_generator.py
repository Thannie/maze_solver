"""
Code responsible for generating a maze.
"""


from maze_cel import MazeCell
import random        

class MazeGenerator:
    """
        Generates a maze using DFS on a grid where walls occupy cells.
        The maze is represented as a 2D array where:
        0 represents a wall,
        1 represents a path.
        The grid dimensions are (2*rows + 1) x (2*cols + 1).
    """
    def __init__(self, rows, cols):
        self.maze_rows = rows   # number of "cell" rows
        self.maze_cols = cols   # number of "cell" columns
        self.full_rows = 2 * rows + 1
        self.full_cols = 2 * cols + 1
        self.grid = [[0 for _ in range(self.full_cols)] for _ in range(self.full_rows)]
    
    def generate_maze(self):

        """
            Generates the maze using a randomized DFS algorithm.
            
            The algorithm starts at the given cell, marks it as visited, and then:
                1. Chooses a random unvisited neighbor.
                2. Removes the wall between the current cell and the neighbor.
                3. Moves to the neighbor and marks it as visited.
                4. If a cell has no unvisited neighbors, it backtracks using the stack.
        """
         # Reset the grid to all walls.
        self.grid = [[0 for _ in range(self.full_cols)] for _ in range(self.full_rows)]

        
        # Start at (1,1) (the first cell in the maze)
        start_r, start_c = 1, 1
        self.grid[start_r][start_c] = 1
        stack = [(start_r, start_c)]
        
        while stack:
            r, c = stack[-1]
            neighbors = []
            # Check in four directions, stepping two cells away.
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 1 <= nr < self.full_rows-1 and 1 <= nc < self.full_cols-1:
                    if self.grid[nr][nc] == 0:
                        neighbors.append((nr, nc, dr, dc))
            if neighbors:
                nr, nc, dr, dc = random.choice(neighbors)
                # Remove the wall between current cell and chosen neighbor.
                self.grid[r + dr//2][c + dc//2] = 1
                self.grid[nr][nc] = 1
                stack.append((nr, nc))
            else:
                stack.pop()
