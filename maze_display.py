import pygame
import sys, time
from maze_solver import AlwaysRightSolver, DFSSolver, AStarSolver, MultiAgentSolver
from button import Button


class MazeDisplay:
    """
    Displays the maze on the left and a side panel with buttons on the right.
    
    New buttons added:
      - "Always Right", "DFS", "A*", "Multi-Agent": to select the solver.
      - "Solve Maze": to manually solve (if auto-solve is off).
      - "Generate Maze": to generate a new maze.
      - "Auto Solve": to toggle automatic solving on updates.
      
    The display also shows the time taken to solve the maze.
    Left-click in the maze sets the start cell (green) and right-click sets the end (red).
    """
    def __init__(self, maze_generator, maze_width, maze_height, panel_width=200,
                 bg_top_color=(30, 30, 30), bg_bottom_color=(0, 0, 0)):
        self.maze_generator = maze_generator
        self.maze_width = maze_width       # Maze drawing area width.
        self.maze_height = maze_height     # Maze drawing area height.
        self.panel_width = panel_width     # Side panel width.
        self.width = maze_width + panel_width
        self.height = maze_height
        self.bg_top_color = bg_top_color
        self.bg_bottom_color = bg_bottom_color
        self.running = True
        self.solution = None
        self.no_solution = False
        self.solver_mode = 'dfs'  # Default solver mode.
        self.auto_solve = False   # Auto-solve toggle.
        self.changed = False      # Flag to indicate a change that requires re-solving.
        self.solve_time = None    # To store the time (in ms) to solve the maze.
        # Default start and end cells.
        self.start_cell = self.maze_generator.grid[0][0]
        self.end_cell = self.maze_generator.grid[self.maze_generator.rows - 1][self.maze_generator.cols - 1]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generator & Solver")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        # Create buttons for the side panel.
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
        # Regenerate the maze using the MazeGenerator's DFS algorithm.
        self.maze_generator.generate_maze(0, 0)
        self.start_cell = self.maze_generator.grid[0][0]
        self.end_cell = self.maze_generator.grid[self.maze_generator.rows - 1][self.maze_generator.cols - 1]
        self.solution = None
        self.no_solution = False
        self.changed = True

    def toggle_auto_solve(self):
        self.auto_solve = not self.auto_solve
        self.auto_solve_button.text = "Auto Solve: ON" if self.auto_solve else "Auto Solve: OFF"
        self.changed = True

    def solve_maze(self):
        # Record the time taken to solve the maze.
        start_time = time.time_ns()
        if self.solver_mode == 'always_right':
            solver = AlwaysRightSolver(self.maze_generator)
            sol = solver.solve(self.start_cell, self.end_cell)
        elif self.solver_mode == 'dfs':
            solver = DFSSolver(self.maze_generator)
            sol = solver.solve(start=self.start_cell, end=self.end_cell)
        elif self.solver_mode == 'astar':
            solver = AStarSolver(self.maze_generator)
            sol = solver.solve(start=self.start_cell, end=self.end_cell)
        elif self.solver_mode == 'multi_agent':
            solver = MultiAgentSolver(self.maze_generator)
            sol = solver.solve()
        end_time = time.time_ns()
        self.solve_time = (end_time - start_time) / 1_000_000  # Solve time in milliseconds.
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
        cell_size = self.start_cell.cell_size
        start_rect = pygame.Rect(self.start_cell.col * cell_size, self.start_cell.row * cell_size, cell_size, cell_size)
        pygame.draw.rect(self.screen, (0, 255, 0), start_rect)
        end_rect = pygame.Rect(self.end_cell.col * cell_size, self.end_cell.row * cell_size, cell_size, cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), end_rect)

    def draw_maze(self):
        for row in self.maze_generator.grid:
            for cell in row:
                cell.draw(self.screen)

    def draw_solution(self):
        if self.solution:
            points = []
            for cell in self.solution:
                x = cell.col * cell.cell_size + cell.cell_size // 2
                y = cell.row * cell.cell_size + cell.cell_size // 2
                points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(self.screen, (0, 0, 255), False, points, 4)
        elif self.no_solution:
            text = self.font.render("No solution found", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.maze_width // 2, self.height // 2))
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
                # Let buttons handle events.
                for button in self.buttons:
                    button.handle_event(event)
                # Allow setting start/end if clicking in the maze area.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < self.maze_width:  # Only process clicks in the maze area.
                        x, y = event.pos
                        col = x // self.maze_generator.cell_size
                        row = y // self.maze_generator.cell_size
                        clicked_cell = self.maze_generator.get_cell(row, col)
                        if clicked_cell:
                            if event.button == 1:  # Left-click sets start.
                                self.start_cell = clicked_cell
                            elif event.button == 3:  # Right-click sets end.
                                self.end_cell = clicked_cell
                            self.solution = None
                            self.no_solution = False
                            self.changed = True

            # Auto-solve if toggled and a change occurred.
            if self.auto_solve and self.changed:
                self.solve_maze()
                self.changed = False

            self.draw_gradient_background()
            self.draw_maze()
            self.draw_start_end()
            self.draw_solution()
            self.draw_buttons()
            self.draw_solve_time()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
        