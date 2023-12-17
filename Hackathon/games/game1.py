# Game 1

import pygame
from test38 import skorlari_kaydet  # Replace with the actual file name

# Accept the additional arguments for game title and button text
def run_game(uid, email, isim, soyisim, oyun_no, game_title, button_text_start):
    pygame.init()
    WIDTH, HEIGHT = 400, 300
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    score = 0

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"{game_title} {oyun_no}")  # Use the passed game title
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score += 1
                elif event.key == pygame.K_ESCAPE:
                    running = False

        win.fill(BLACK)
        text = font.render(f"Skor: {score}", True, WHITE)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    skorlari_kaydet(uid, email, isim, soyisim, oyun_no, score)