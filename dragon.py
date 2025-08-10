import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino")

# Load images
dragon_img = pygame.image.load("dragon.png")
dragon_img = pygame.transform.scale(dragon_img, (60, 60))

cactus_img = pygame.image.load("cactus.png")
cactus_img = pygame.transform.scale(cactus_img, (40, 60))

# Colors
SKY_BLUE = (225, 225, 225)
GROUND_COLOR = (83, 53, 10)
TEXT_COLOR = (0, 0, 0)
SHADOW_COLOR = (180, 180, 180)

# Fonts
font = pygame.font.SysFont("Arial", 36, bold=True)

# Game variables
clock = pygame.time.Clock()
gravity = 1
jump_power = 15
obstacle_speed = 7
score = 0
game_over = False

# Dino (player)
dino_rect = pygame.Rect(100, HEIGHT - 100, 60, 60)
dino_y_velocity = 0
is_jumping = False

# Obstacles
obstacles = []
SPAWN_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_OBSTACLE, 1500)


def reset_game():
    global score, game_over, obstacle_speed, dino_rect, dino_y_velocity, is_jumping, obstacles
    score = 0
    game_over = False
    obstacle_speed = 7
    dino_rect.y = HEIGHT - 100
    dino_y_velocity = 0
    is_jumping = False
    obstacles.clear()


def draw_text(text, size, color, x, y, shadow=True):
    font_obj = pygame.font.SysFont("Arial", size, bold=True)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))

    if shadow:
        shadow_surface = font_obj.render(text, True, SHADOW_COLOR)
        win.blit(shadow_surface, (x + 2, y + 2))
    win.blit(text_surface, text_rect)


def draw_window():
    win.fill(SKY_BLUE)

    # Ground
    pygame.draw.rect(win, GROUND_COLOR, (0, HEIGHT - 40, WIDTH, 40))
    pygame.draw.line(win, TEXT_COLOR, (0, HEIGHT - 40), (WIDTH, HEIGHT - 40), 2)

    # Dragon
    win.blit(dragon_img, (dino_rect.x, dino_rect.y))

    # Obstacles
    for obs in obstacles:
        win.blit(cactus_img, (obs.x, obs.y))

    # Score (top-left)
    draw_text(f"Score: {score}", 30, TEXT_COLOR, 10, 10)

    if game_over:
        # Nicer fonts
        big_font = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
        medium_font = pygame.font.SysFont("Comic Sans MS", 40)
        small_font = pygame.font.SysFont("Comic Sans MS", 30)

        # Render texts
        msg = big_font.render("GAME OVER", True, (255, 0, 0))
        score_msg = medium_font.render(f"Your Score: {score}", True, TEXT_COLOR)
        restart_msg = small_font.render("Press R to Restart", True, TEXT_COLOR)
        sub_msg = small_font.render("Subscribe Tee Chungs :)", True, (0, 100, 200))

        # Center positions
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        score_rect = score_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        restart_rect = restart_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        sub_rect = sub_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

        # Blit to screen
        win.blit(msg, msg_rect)
        win.blit(score_msg, score_rect)
        win.blit(restart_msg, restart_rect)
        win.blit(sub_msg, sub_rect)

    pygame.display.update()


# Game loop
while True:
    clock.tick(60)

    if not game_over:
        score += 1
        if score % 100 == 0:
            obstacle_speed += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWN_OBSTACLE and not game_over:
            height_offset = random.choice([0, 5, 10])
            x_offset = random.randint(0, 40)
            obstacle = pygame.Rect(WIDTH + x_offset, HEIGHT - 100 - height_offset, 40, 60)
            obstacles.append(obstacle)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not is_jumping and not game_over:
                dino_y_velocity = -jump_power
                is_jumping = True
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # Apply gravity
        dino_y_velocity += gravity
        dino_rect.y += dino_y_velocity

        if dino_rect.y >= HEIGHT - 100:
            dino_rect.y = HEIGHT - 100
            is_jumping = False

        # Move obstacles
        for obs in obstacles:
            obs.x -= obstacle_speed

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs.x > -40]

        # Collision detection
        for obs in obstacles:
            if dino_rect.colliderect(obs):
                game_over = True

    draw_window()
