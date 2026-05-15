import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
LIGHT_GRAY = (50, 50, 50)
GREEN = (39, 174, 96)
DARK_GREEN = (27, 120, 66)
RED = (231, 76, 60)
DARK_RED = (169, 50, 38)

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake starting position
snake = [(15, 15), (14, 15), (13, 15)]
direction = (1, 0)  # Moving right

def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (WINDOW_WIDTH, y))

def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        color = DARK_GREEN if i == 0 else GREEN
        pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, GRAY, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_food(food):
    x, y = food
    pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, DARK_RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake.insert(0, new_head)
    snake.pop()
    return snake

food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    snake = move_snake(snake, direction)

    screen.fill(GRAY)
    draw_grid()
    draw_snake(snake)
    draw_food(food)
    pygame.display.flip()
    clock.tick(FPS)