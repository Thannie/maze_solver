import pygame


class MazeCell:
    """
    Represents a single cell within the maze grid.
    
    Each cell keeps track of its grid position, the status of its walls,
    and whether it has been visited.
    """
    def __init__(self, row, col, cell_size):
        """
        Initializes a maze cell.
        
        Parameters:
            row (int): Row index of the cell.
            col (int): Column index of the cell.
            cell_size (int): Size of the cell in pixels.
        """
        self.row = row
        self.col = col
        self.cell_size = cell_size
        # Each cell starts with all walls intact.
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def __lt__(self, other):
        """
        Less-than comparison method to allow MazeCell objects to be compared.
        
        This is necessary for the A* algorithm when f-scores are equal.
        """
        if not isinstance(other, MazeCell):
            return NotImplemented
        return (self.row, self.col) < (other.row, other.col)

    def draw(self, surface, wall_color=(255, 255, 255)):
        """
        Draws the cell's walls on the given surface.
        
        Parameters:
            surface (pygame.Surface): The surface on which to draw the cell.
            wall_color (tuple): The RGB color for the walls.
        """
        x = self.col * self.cell_size
        y = self.row * self.cell_size

        if self.walls['top']:
            pygame.draw.line(surface, wall_color, (x, y), (x + self.cell_size, y), 2)
        if self.walls['right']:
            pygame.draw.line(surface, wall_color, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        if self.walls['bottom']:
            pygame.draw.line(surface, wall_color, (x + self.cell_size, y + self.cell_size), (x, y + self.cell_size), 2)
        if self.walls['left']:
            pygame.draw.line(surface, wall_color, (x, y + self.cell_size), (x, y), 2)

