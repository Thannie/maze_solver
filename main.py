"""
A maze solver / generator

Controls:
 - 1,2,3,4: Select a solver
 - s: Solve the maze
 - Left click: Change start
 - Right click: Change end
 
Made by Jonathan
"""


from maze_generator import MazeGenerator
from maze_display import MazeDisplay


from maze_generator import MazeGenerator
from maze_display import MazeDisplay

if __name__ == "__main__":
    cell_size = 20
    cols = 40
    rows = 30

    maze_generator = MazeGenerator(rows, cols, cell_size)
    maze_generator.generate_maze()

    maze_width = cols * cell_size
    maze_height = rows * cell_size
    panel_width = 200  # Extra space for buttons

    maze_display = MazeDisplay(maze_generator, maze_width, maze_height, panel_width)
    maze_display.run()

    