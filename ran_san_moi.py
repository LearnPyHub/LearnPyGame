import pygame
import random
import time

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Tạo màn hình game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rắn săn mồi")

# Clock để kiểm soát tốc độ
clock = pygame.time.Clock()

# Hàm hiển thị thông báo với kích thước font động
def show_message(text, color, x, y, font_ratio=0.1):
    """
    Hiển thị thông báo trên màn hình
    - text: Nội dung thông báo
    - color: Màu sắc
    - x, y: Tọa độ hiển thị
    - font_ratio: Tỷ lệ kích thước chữ so với chiều cao màn hình
    """
    font_size = int(HEIGHT * font_ratio)  # Tính kích thước font theo tỷ lệ
    font = pygame.font.SysFont("Arial", font_size)
    message = font.render(text, True, color)
    text_rect = message.get_rect(center=(x, y))  # Căn giữa thông báo
    screen.blit(message, text_rect)

# Màn hình chào mừng
def welcome_screen():
    screen.fill(BLACK)
    show_message("Chào mừng đến với Rắn Săn Mồi!", GREEN, WIDTH // 2, HEIGHT // 3, font_ratio=0.08)
    show_message("Nhấn SPACE để bắt đầu", WHITE, WIDTH // 2, HEIGHT // 2, font_ratio=0.06)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Màn hình Game Over
def game_over_screen(score):
    screen.fill(BLACK)
    show_message("Game Over!", RED, WIDTH // 2, HEIGHT // 3, font_ratio=0.1)
    show_message(f"Điểm của bạn: {score}", WHITE, WIDTH // 2, HEIGHT // 2, font_ratio=0.07)
    show_message("Nhấn SPACE để chơi lại", GREEN, WIDTH // 2, HEIGHT // 1.5, font_ratio=0.06)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Hàm chính
def main():
    # Vị trí ban đầu của rắn
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    score = 0

    # Tạo thức ăn
    food_x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    food_y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    food = (food_x, food_y)

    running = True
    while running:
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Điều khiển rắn
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        if keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        if keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        if keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        # Cập nhật vị trí rắn
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        if direction == "DOWN":
            head_y += CELL_SIZE
        if direction == "LEFT":
            head_x -= CELL_SIZE
        if direction == "RIGHT":
            head_x += CELL_SIZE
        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Kiểm tra rắn ăn thức ăn
        if new_head == food:
            score += 1
            food_x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            food_y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            food = (food_x, food_y)
        else:
            snake.pop()

        # Kiểm tra va chạm
        if (
            head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
            or new_head in snake[1:]
        ):
            game_over_screen(score)
            return

        # Vẽ màn hình game
        screen.fill(BLACK)
        # Vẽ rắn
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Vẽ thức ăn
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Hiển thị điểm
        score_text = pygame.font.SysFont("Arial", 25).render(f"Điểm: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)  # Tốc độ game (10 FPS)

# Chạy game
while True:
    welcome_screen()
    main()
