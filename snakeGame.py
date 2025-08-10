import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
colors = [
    (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
    (0, 255, 255), (0, 0, 255), (139, 0, 255)
]
BG_COLOR = (180, 225, 240)

# Screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rainbow Snake Game")

# Clock & font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 40, bold=True)

# Snake settings
snake_block = 20
snake_speed = 10

def draw_snake(snake):
    for i, block in enumerate(snake):
        pygame.draw.circle(screen, colors[i % len(colors)], (block[0] + 10, block[1] + 10), 10)

def is_collision(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def game_over_screen(score):
    screen.fill(BG_COLOR)

    # Use nicer fonts
    big_font = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
    medium_font = pygame.font.SysFont("Comic Sans MS", 40)
    small_font = pygame.font.SysFont("Comic Sans MS", 35)

    # Render text
    msg = big_font.render("Game Over!", True, (255, 0, 0))
    score_msg = medium_font.render(f"Score: {score}", True, (0, 0, 0))
    restart_msg = small_font.render("Press SPACE to Restart", True, (0, 0, 0))
    sub_msg = small_font.render("Subscribe Tee Chungs :)", True, (0, 0, 0))

    # Get rectangles for centering
    msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    score_rect = score_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    restart_rect = restart_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    sub_rect = sub_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

    # Draw text
    screen.blit(msg, msg_rect)
    screen.blit(score_msg, score_rect)
    screen.blit(restart_msg, restart_rect)
    screen.blit(sub_msg, sub_rect)

    pygame.display.flip()

    # Wait for restart or quit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Restart the game

def main():
    snake = [(100, 100)]
    direction = "RIGHT"
    change_to = direction
    food = (random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block))
    score = 0
    running = True

    while running:
        screen.fill(BG_COLOR)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"

        direction = change_to

        # Move snake
        x, y = snake[0]
        if direction == "UP":
            y -= snake_block
        elif direction == "DOWN":
            y += snake_block
        elif direction == "LEFT":
            x -= snake_block
        elif direction == "RIGHT":
            x += snake_block

        new_head = (x, y)

        # Check wall collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_over_screen(score)
            return  # Restart from main()

        # Check self collision
        if new_head in snake:
            game_over_screen(score)
            return  # Restart from main()

        snake.insert(0, new_head)

        # Check if snake eats food
        if is_collision(new_head, food):
            score += 1
            food = (random.randrange(0, WIDTH, snake_block), random.randrange(0, HEIGHT, snake_block))
        else:
            snake.pop()

        # Draw food
        pygame.draw.circle(screen, (0, 0, 0), (food[0] + 10, food[1] + 10), 10)

        # Draw snake
        draw_snake(snake)

        # Draw score
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(snake_speed)

# Main game loop with restart
while True:
    main()
