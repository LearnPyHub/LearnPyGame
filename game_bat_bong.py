import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Bắt Bóng")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, YELLOW]

# FPS
clock = pygame.time.Clock()
FPS = 60

# Font chữ
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

# Giao diện chào mừng
def show_welcome_screen():
    screen.fill(WHITE)
    title = font.render("Chào mừng đến với Game Bắt Bóng!", True, BLACK)
    instruction = small_font.render("Nhấn phím SPACE để bắt đầu", True, BLACK)
    credit = small_font.render("Code game: ThongTNM", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(credit, (WIDTH // 2 - credit.get_width() // 2, HEIGHT - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Giao diện kết thúc
def show_game_over_screen(score):
    screen.fill(WHITE)
    game_over = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"Điểm của bạn: {score}", True, BLACK)
    retry = small_font.render("Nhấn phím SPACE để chơi lại hoặc ESC để thoát", True, BLACK)
    credit = small_font.render("Code game: ThongTNM", True, BLACK)
    screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(retry, (WIDTH // 2 - retry.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(credit, (WIDTH // 2 - credit.get_width() // 2, HEIGHT - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Chơi lại
                if event.key == pygame.K_ESCAPE:
                    return False  # Thoát game

# Hàm chơi game chính
def play_game():
    # Vật thể
    ball_radius = 20
    ball_x = random.randint(ball_radius, WIDTH - ball_radius)
    ball_y = -ball_radius
    ball_speed = 5
    ball_color = random.choice(COLORS)

    player_width = 100
    player_height = 20
    player_x = (WIDTH - player_width) // 2
    player_y = HEIGHT - player_height - 10
    player_speed = 10

    # Vật phẩm hỗ trợ
    powerup_radius = 15
    powerup_x = random.randint(powerup_radius, WIDTH - powerup_radius)
    powerup_y = -powerup_radius
    powerup_speed = 3
    powerup_type = random.choice(["shield", "extend"])
    powerup_timer = 0

    # Trạng thái hỗ trợ
    shield_active = False
    shield_timer = 0
    extend_active = False
    extend_timer = 0

    # Điểm số
    score = 0

    # Game loop
    running = True
    while running:
        # Xóa màn hình
        screen.fill(WHITE)

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Điều khiển thanh
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Cập nhật vị trí bóng
        ball_y += ball_speed

        # Kiểm tra va chạm bóng
        if (player_x < ball_x < player_x + player_width) and (player_y < ball_y + ball_radius < player_y + player_height):
            score += 1
            ball_x = random.randint(ball_radius, WIDTH - ball_radius)
            ball_y = -ball_radius
            ball_speed += 0.5
            ball_color = random.choice(COLORS)

        # Kiểm tra bóng rơi
        if ball_y > HEIGHT:
            if shield_active:
                shield_active = False  # Tắt chế độ bảo vệ
                ball_x = random.randint(ball_radius, WIDTH - ball_radius)
                ball_y = -ball_radius
            else:
                return score

        # Cập nhật vị trí vật phẩm
        powerup_y += powerup_speed

        # Kiểm tra va chạm vật phẩm
        if (player_x < powerup_x < player_x + player_width) and (player_y < powerup_y + powerup_radius < player_y + player_height):
            if powerup_type == "shield":
                shield_active = True
                shield_timer = pygame.time.get_ticks()
            elif powerup_type == "extend":
                extend_active = True
                extend_timer = pygame.time.get_ticks()
                player_width = int(player_width * 1.5)
            powerup_y = -powerup_radius
            powerup_x = random.randint(powerup_radius, WIDTH - powerup_radius)
            powerup_type = random.choice(["shield", "extend"])

        # Kiểm tra thời gian hỗ trợ
        current_time = pygame.time.get_ticks()
        if shield_active and current_time - shield_timer > 5000:  # 5 giây
            shield_active = False
        if extend_active and current_time - extend_timer > 5000:  # 5 giây
            extend_active = False
            player_width = int(player_width / 1.5)

        # Nếu vật phẩm rơi ra khỏi màn hình, tái tạo
        if powerup_y > HEIGHT:
            powerup_y = -powerup_radius
            powerup_x = random.randint(powerup_radius, WIDTH - powerup_radius)
            powerup_type = random.choice(["shield", "extend"])

        # Vẽ bóng
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

        # Vẽ vật phẩm hỗ trợ
        if powerup_type == "shield":
            pygame.draw.circle(screen, GREEN, (powerup_x, powerup_y), powerup_radius)
        elif powerup_type == "extend":
            pygame.draw.circle(screen, YELLOW, (powerup_x, powerup_y), powerup_radius)

        # Vẽ thanh
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Hiển thị điểm và trạng thái hỗ trợ
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        shield_text = small_font.render(f"Shield: {'ON' if shield_active else 'OFF'}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(shield_text, (10, 40))

        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(FPS)

# Chạy game
while True:
    show_welcome_screen()
    score = play_game()
    if not show_game_over_screen(score):
        break
