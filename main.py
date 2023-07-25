import pygame
import random

# Define colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# Define block shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

class TetrisGame:
    def __init__(self, window_width, window_height, grid_width, grid_height):
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.block_size = min(window_width // grid_width, window_height // grid_height)
        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.choice([CYAN, YELLOW, MAGENTA, GREEN, RED, ORANGE, BLUE])
        self.current_x = grid_width // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.rotated = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.current_x > 0:
                self.current_x -= 1
            if keys[pygame.K_RIGHT] and self.current_x + len(self.current_shape[0]) < self.grid_width:
                self.current_x += 1
            if keys[pygame.K_DOWN] and self.current_y + len(self.current_shape) < self.grid_height:
                self.current_y += 1
            if keys[pygame.K_UP] and not self.rotated:
                self.rotate_shape()
                self.rotated = True
            if not keys[pygame.K_UP]:
                self.rotated = False

            self.update_grid()
            self.clear_complete_rows()
            self.draw_grid()

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

    def rotate_shape(self):
        self.current_shape = list(zip(*reversed(self.current_shape)))

    def update_grid(self):
        # Reset the grid
        self.grid = [[BLACK for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Update the grid with the current shape
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[0])):
                if self.current_shape[row][col] == 1:
                    self.grid[self.current_y + row][self.current_x + col] = self.current_color

    def clear_complete_rows(self):
        for row in range(self.grid_height):
            if all(color != BLACK for color in self.grid[row]):
                del self.grid[row]
                self.grid.insert(0, [BLACK] * self.grid_width)

    def draw_grid(self):
        self.window.fill(BLACK)
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                pygame.draw.rect(self.window, self.grid[row][col],
                                 (col * self.block_size, row * self.block_size, self.block_size, self.block_size))

if __name__ == "__main__":
    game = TetrisGame(800, 600, 10, 20)
    game.run()
