"""
Code responsible for generating a maze.
"""


from maze_cel import MazeCell
import random


class MazeGenerator:
    """
    Implements maze generation using a randomized depth-first search algorithm.
    """
    def __init__(self, rows, cols, cell_size):
        """
        Initializes the maze grid and stack for the DFS algorithm.
        
        Parameters:
            rows (int): Number of rows in the maze.
            cols (int): Number of columns in the maze.
            cell_size (int): Size of each cell in pixels.
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        # Create a grid (2D list) of MazeCell objects.
        self.grid = [[MazeCell(r, c, cell_size) for c in range(cols)] for r in range(rows)]
        # Stack to hold the path for backtracking.
        self.stack = []

    def get_cell(self, row, col):
        """
        Retrieves the cell at the specified row and column.
        
        Returns:
            MazeCell if the indices are valid, otherwise None.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_unvisited_neighbors(self, cell):
        """
        Returns a list of unvisited neighboring cells along with the direction from the current cell.
        
        The directions are: 'top', 'right', 'bottom', 'left'.
        
        Parameters:
            cell (MazeCell): The current cell.
            
        Returns:
            List of tuples (neighbor_cell, direction).
        """
        neighbors = []
        row, col = cell.row, cell.col

        # Top neighbor
        neighbor = self.get_cell(row - 1, col)
        if neighbor and not neighbor.visited:
            neighbors.append((neighbor, 'top'))
        # Right neighbor
        neighbor = self.get_cell(row, col + 1)
        if neighbor and not neighbor.visited:
            neighbors.append((neighbor, 'right'))
        # Bottom neighbor
        neighbor = self.get_cell(row + 1, col)
        if neighbor and not neighbor.visited:
            neighbors.append((neighbor, 'bottom'))
        # Left neighbor
        neighbor = self.get_cell(row, col - 1)
        if neighbor and not neighbor.visited:
            neighbors.append((neighbor, 'left'))

        return neighbors

    def remove_walls(self, current, neighbor, direction):
        """
        Removes the wall between the current cell and the neighbor in the given direction.
        
        Parameters:
            current (MazeCell): The current cell.
            neighbor (MazeCell): The neighboring cell.
            direction (str): The direction from current to neighbor ('top', 'right', 'bottom', or 'left').
        """
        if direction == 'top':
            current.walls['top'] = False
            neighbor.walls['bottom'] = False
        elif direction == 'right':
            current.walls['right'] = False
            neighbor.walls['left'] = False
        elif direction == 'bottom':
            current.walls['bottom'] = False
            neighbor.walls['top'] = False
        elif direction == 'left':
            current.walls['left'] = False
            neighbor.walls['right'] = False

    def generate_maze(self, start_row=0, start_col=0):
        """
        Generates the maze using a randomized DFS algorithm.
        
        The algorithm starts at the given cell, marks it as visited, and then:
            1. Chooses a random unvisited neighbor.
            2. Removes the wall between the current cell and the neighbor.
            3. Moves to the neighbor and marks it as visited.
            4. If a cell has no unvisited neighbors, it backtracks using the stack.
        
        Parameters:
            start_row (int): The starting cell's row index.
            start_col (int): The starting cell's column index.
        """

        # Reset each cell's visited status and restore all walls.
        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        # Clear the stack.
        self.stack = []


        current = self.get_cell(start_row, start_col)
        current.visited = True
        self.stack.append(current)

        while self.stack:
            current = self.stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                # Choose a random unvisited neighbor
                neighbor, direction = random.choice(neighbors)
                # Remove the wall between the current cell and the neighbor
                self.remove_walls(current, neighbor, direction)
                neighbor.visited = True
                self.stack.append(neighbor)
            else:
                # Backtrack if no unvisited neighbors are available
                self.stack.pop()
