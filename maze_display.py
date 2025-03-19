import pygame
import sys, time
from maze_solver import GridAStarSolver, GridDFSSolver
from button import Button


class MazeDisplay:
    """
    Displays the maze (now a 2D grid) on the left and a side panel with buttons on the right.
    In the grid, 0 is a wall and 1 is a path.
    You can change the start (green) and end (red) points by clicking in the maze.
    """
    def __init__(self, maze_generator, cell_size, panel_width=200,
                 wall_color=(0, 0, 0), path_color=(255, 255, 255)):
        self.maze_generator = maze_generator  # uses new grid-based maze
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.path_color = path_color
        self.panel_width = panel_width
        self.maze_width = maze_generator.full_cols * cell_size
        self.maze_height = maze_generator.full_rows * cell_size
        self.width = self.maze_width + panel_width
        self.height = self.maze_height
        self.running = True
        self.solution = None
        self.no_solution = False
        self.solver_mode = 'dfs'  # "dfs" or "astar"
        self.auto_solve = False
        self.changed = False
        self.solve_time = None
        # Start and end are stored as (row, col) in grid coordinates.
        self.start_cell = (1, 1)
        self.end_cell = (maze_generator.full_rows - 2, maze_generator.full_cols - 2)

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generator & Solver (Grid)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        # Button dimensions and positions in the side panel.
        button_width = self.panel_width - 20
        button_height = 40
        x = self.maze_width + 10  # Panel's x-start.
        y = 20
        gap = 10

        # Helper to set the solver mode.
        def set_solver_mode(mode):
            def inner():
                self.solver_mode = mode
                self.solution = None
                self.no_solution = False
                self.changed = True
            return inner

        # Create solver mode buttons with associated mode.
        self.buttons.append(Button((x, y, button_width, button_height), "Always Right", set_solver_mode("always_right"), mode="always_right"))
        y += button_height + gap
        self.buttons.append(Button((x, y, button_width, button_height), "DFS", set_solver_mode("dfs"), mode="dfs"))
        y += button_height + gap
        self.buttons.append(Button((x, y, button_width, button_height), "A*", set_solver_mode("astar"), mode="astar"))
        y += button_height + gap
        self.buttons.append(Button((x, y, button_width, button_height), "Multi-Agent", set_solver_mode("multi_agent"), mode="multi_agent"))
        y += button_height + gap

        # Manual solve button.
        self.buttons.append(Button((x, y, button_width, button_height), "Solve Maze", self.solve_maze))
        y += button_height + gap

        # Generate Maze button.
        self.buttons.append(Button((x, y, button_width, button_height), "Generate Maze", self.generate_new_maze))
        y += button_height + gap

        # Auto Solve toggle button.
        self.auto_solve_button = Button((x, y, button_width, button_height), "Auto Solve: OFF", self.toggle_auto_solve)
        self.buttons.append(self.auto_solve_button)
        y += button_height + gap

    def generate_new_maze(self):
        self.maze_generator.generate_maze()
        self.start_cell = (1, 1)
        self.end_cell = (self.maze_generator.full_rows - 2, self.maze_generator.full_cols - 2)
        self.solution = None
        self.no_solution = False
        self.changed = True

    def toggle_auto_solve(self):
        self.auto_solve = not self.auto_solve
        self.auto_solve_button.text = "Auto Solve: ON" if self.auto_solve else "Auto Solve: OFF"
        self.changed = True

    def toggle_auto_solve(self):
        self.auto_solve = not self.auto_solve
        self.auto_solve_button.text = "Auto Solve: ON" if self.auto_solve else "Auto Solve: OFF"
        self.changed = True

    def solve_maze(self):
        start = self.start_cell
        end = self.end_cell
        start_time = time.time_ns()
        if self.solver_mode == 'dfs':
            solver = GridDFSSolver(self.maze_generator.grid)
            sol = solver.solve(start, end)
        elif self.solver_mode == 'astar':
            solver = GridAStarSolver(self.maze_generator.grid)
            sol = solver.solve(start, end)
        else:
            solver = GridDFSSolver(self.maze_generator.grid)
            sol = solver.solve(start, end)
        end_time = time.time_ns()
        self.solve_time = (end_time - start_time) / 1_000_00  # in milliseconds
        if sol:
            self.solution = sol
            self.no_solution = False
        else:
            self.solution = None
            self.no_solution = True

    def draw_gradient_background(self):
        # Draw gradient for the maze area.
        for y in range(self.height):
            ratio = y / self.height
            r = int(self.bg_top_color[0] * (1 - ratio) + self.bg_bottom_color[0] * ratio)
            g = int(self.bg_top_color[1] * (1 - ratio) + self.bg_bottom_color[1] * ratio)
            b = int(self.bg_top_color[2] * (1 - ratio) + self.bg_bottom_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.maze_width, y))
        # Fill the side panel with a solid color.
        panel_color = (50, 50, 50)
        panel_rect = pygame.Rect(self.maze_width, 0, self.panel_width, self.height)
        pygame.draw.rect(self.screen, panel_color, panel_rect)

    def draw_start_end(self):
        sr, sc = self.start_cell
        er, ec = self.end_cell
        start_rect = pygame.Rect(sc * self.cell_size, sr * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (0, 255, 0), start_rect)
        end_rect = pygame.Rect(ec * self.cell_size, er * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), end_rect)

    def draw_maze(self):
        for i, row in enumerate(self.maze_generator.grid):
            for j, cell in enumerate(row):
                color = self.path_color if cell == 1 else self.wall_color
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def draw_solution(self):
        if self.solution:
            points = []
            for r, c in self.solution:
                x = c * self.cell_size + self.cell_size // 2
                y = r * self.cell_size + self.cell_size // 2
                points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(self.screen, (0, 0, 255), False, points, 4)
        elif self.no_solution:
            text = self.font.render("No solution found", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.maze_width // 2, self.maze_height // 2))
            self.screen.blit(text, text_rect)

    def draw_buttons(self):
        # Update selected state for solver mode buttons.
        for button in self.buttons:
            if button.mode is not None:
                button.selected = (self.solver_mode == button.mode)
            button.draw(self.screen)

    def draw_solve_time(self):
        # Draw the solve time at the bottom of the panel.
        if self.solve_time is not None:
            text = self.font.render(f"Solve Time: {self.solve_time} ms", True, (255, 255, 255))
            text_rect = text.get_rect(midbottom=(self.maze_width + self.panel_width // 2, self.height - 20))
            self.screen.blit(text, text_rect)
        
        else:
            text = self.font.render(f"Solve Time: N/A ms", True, (255, 255, 255))
            text_rect = text.get_rect(midbottom=(self.maze_width + self.panel_width // 2, self.height - 20))
            self.screen.blit(text, text_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons:
                    button.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < self.maze_width:
                        x, y = event.pos
                        col = x // self.cell_size
                        row = y // self.cell_size
                        # Only allow changing start/end on a path cell.
                        if self.maze_generator.grid[row][col] == 1:
                            if event.button == 1:
                                self.start_cell = (row, col)
                            elif event.button == 3:
                                self.end_cell = (row, col)
                            self.solution = None
                            self.no_solution = False
                            self.changed = True
            if self.auto_solve and self.changed:
                self.solve_maze()
                self.changed = False
            self.screen.fill((0, 0, 0))
            self.draw_maze()
            self.draw_start_end()
            self.draw_solution()
            self.draw_buttons()
            self.draw_solve_time()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
        