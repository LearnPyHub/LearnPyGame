import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Tốc độ khung hình
clock = pygame.time.Clock()
FPS = 60

# Tạo các biến chính
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 4
PIPE_GAP = 200  # Tăng khoảng cách giữa các cột

# Tải hình ảnh
bird_image = pygame.Surface((30, 30))
bird_image.fill(YELLOW)  # Màu vàng

pipe_image = pygame.Surface((50, SCREEN_HEIGHT))
pipe_image.fill(GREEN)  # Màu xanh lá

# Lớp Bird
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = bird_image.get_rect(center=(self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):
        screen.blit(bird_image, self.rect)

# Lớp Pipe
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top_rect = pipe_image.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = pipe_image.get_rect(midtop=(self.x, self.height + PIPE_GAP))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.midbottom = (self.x, self.height)
        self.bottom_rect.midtop = (self.x, self.height + PIPE_GAP)

    def draw(self):
        screen.blit(pipe_image, self.top_rect)
        screen.blit(pipe_image, self.bottom_rect)

    def off_screen(self):
        return self.x < -50

# Kiểm tra va chạm
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    if bird.y <= 0 or bird.y >= SCREEN_HEIGHT:
        return True
    return False

# Màn hình chào mừng
def welcome_screen():
    font = pygame.font.SysFont(None, 48)
    running = True
    while running:
        screen.fill(WHITE)
        text = font.render("Welcome to Flappy Bird!", True, BLACK)
        instruction = font.render("Press SPACE to Start", True, BLACK)

        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

# Màn hình Game Over
def game_over_screen(score):
    font = pygame.font.SysFont(None, 48)
    running = True
    while running:
        screen.fill(WHITE)
        text = font.render("Game Over!", True, BLACK)
        score_text = font.render(f"Your Score: {score}", True, BLACK)
        instruction = font.render("Press SPACE to Restart", True, BLACK)

        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 1.5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

# Hàm chính
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
    score = 0
    game_started = False

    while True:
        if not game_started:
            welcome_screen()
            bird = Bird()
            pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(3)]
            score = 0
            game_started = True

        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Cập nhật Bird
        bird.update()

        # Cập nhật Pipes
        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe_image.get_width() < bird.x and not hasattr(pipe, "scored"):
                score += 1
                pipe.scored = True

        # Xóa pipe nếu ra khỏi màn hình và thêm pipe mới
        if pipes[0].off_screen():
            pipes.pop(0)
            pipes.append(Pipe(SCREEN_WIDTH + 300))

        # Kiểm tra va chạm
        if check_collision(bird, pipes):
            game_over_screen(score)
            game_started = False

        # Vẽ Pipes
        for pipe in pipes:
            pipe.draw()

        # Vẽ Bird
        bird.draw()

        # Hiển thị điểm
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
