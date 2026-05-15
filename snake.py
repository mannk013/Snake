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
BLACK      = (0, 0, 0)
GRAY       = (25, 25, 35)
LIGHT_GRAY = (40, 40, 55)
GREEN      = (46, 204, 113)
DARK_GREEN = (39, 174, 96)
HEAD_GREEN = (26, 188, 156)
RED        = (231, 76, 60)
DARK_RED   = (192, 57, 43)
WHITE      = (255, 255, 255)
YELLOW     = (241, 196, 15)

# Setup window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 36, bold=True)
font_small = pygame.font.SysFont("consolas", 24)

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
        if i == 0:
            # Head — rounded and different color
            color = HEAD_GREEN
        else:
            # Body — gradient effect
            fade = max(0, 255 - i * 8)
            color = (0, min(255, 100 + i * 3), min(255, 80 + i * 5))

        rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.rect(screen, color, rect, border_radius=4)

        # Eyes on head
        if i == 0:
            pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + 6, y * GRID_SIZE + 6), 3)
            pygame.draw.circle(screen, WHITE, (x * GRID_SIZE + 14, y * GRID_SIZE + 6), 3)
            pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 7, y * GRID_SIZE + 7), 1)
            pygame.draw.circle(screen, BLACK, (x * GRID_SIZE + 15, y * GRID_SIZE + 7), 1)

def draw_food(food):
    x, y = food
    # Apple body
    pygame.draw.circle(screen, RED,
        (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
        GRID_SIZE // 2 - 2)
    # Apple shine
    pygame.draw.circle(screen, (255, 120, 100),
        (x * GRID_SIZE + 6, y * GRID_SIZE + 6), 3)
def check_collision(snake):
    head = snake[0]
    # Wall collision
    if head[0] < 0 or head[0] >= GRID_WIDTH:
        return True
    if head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    # Self collision
    if head in snake[1:]:
        return True
    return False

def check_food(snake, food, score):
    if snake[0] == food:
        new_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        snake.append(snake[-1])
        score += 1
        return new_food, score
    return food, score

def draw_score(score):
    # Background bar
    pygame.draw.rect(screen, (35, 35, 50), (0, 0, WINDOW_WIDTH, 36))
    text = font_small.render(f"🐍 Score: {score}", True, YELLOW)
    screen.blit(text, (10, 8))

def draw_game_over(score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    text = font.render("GAME OVER", True, (231, 76, 60))
    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 220))

    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 290))

    restart_text = font_small.render("Press R to restart", True, (200, 200, 200))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 340))

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    snake.insert(0, new_head)
    snake.pop()
    return snake

food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    snake = [(15, 15), (14, 15), (13, 15)]
                    direction = (1, 0)
                    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                    score = 0
                    game_over = False
            else:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    if not game_over:
        snake = move_snake(snake, direction)

        if check_collision(snake):
            game_over = True

        food, score = check_food(snake, food, score)

    screen.fill(GRAY)
    draw_grid()
    draw_snake(snake)
    draw_food(food)
    draw_score(score)

    if game_over:
        draw_game_over(score)

    pygame.display.flip()
    clock.tick(FPS)