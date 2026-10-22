import pygame
import random

# Screen setup
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont(None, 52)

# Paddle settings
paddle_width = 18
paddle_height = 120
paddle_speed = 8

# Left paddle
left_paddle = pygame.Rect(30, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Right paddle (computer)
right_paddle = pygame.Rect(WIDTH - 30 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed_x = 7
ball_speed_y = 7

# Scores
left_score = 0
right_score = 0

def reset_ball(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = direction * random.choice([6, 7, 8])
    ball_speed_y = random.choice([-5, -4, -3, 3, 4, 5])

def draw_score():
    score_text = font.render(f"{left_score}   {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse control for left paddle
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < WIDTH // 2:
        left_paddle.centery = mouse_y

    # Keyboard control for left paddle (arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN]:
        left_paddle.y += paddle_speed

    # Keep paddles inside screen
    left_paddle.y = max(0, min(HEIGHT - paddle_height, left_paddle.y))
    right_paddle.y = max(0, min(HEIGHT - paddle_height, right_paddle.y))

    # Computer AI for right paddle
    if ball.centery < right_paddle.centery:
        right_paddle.y -= 5
    elif ball.centery > right_paddle.centery:
        right_paddle.y += 5

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall collision (top and bottom)
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle collision
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        ball.left = left_paddle.right
        ball_speed_x = abs(ball_speed_x) + 0.5
        ball_speed_y += (ball.centery - left_paddle.centery) * 0.15

    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        ball.right = right_paddle.left
        ball_speed_x = -abs(ball_speed_x) - 0.5
        ball_speed_y += (ball.centery - right_paddle.centery) * 0.15

    # Scoring
    if ball.left <= 0:
        right_score += 1
        reset_ball(1)
    elif ball.right >= WIDTH:
        left_score += 1
        reset_ball(-1)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    draw_score()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()