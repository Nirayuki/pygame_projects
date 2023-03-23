import pygame
import os

pygame.init()
# Variaveis ------------------------------------------------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Player movement
MOVE_RIGHT = False
MOVE_LEFT = False
GRAVITY = 0

PLAYER_LOCATION = [50, 50]

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Template Pygame init")

# Color ------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)

# Sound ------------------------------------------------------------------


# Images ------------------------------------------------------------------
PLAYER_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'player.png'))
PLAYER = pygame.transform.scale(PLAYER_IMG, (100, 100))

# Funções ------------------------------------------------------------------


# Class ------------------------------------------------------------------


# Main ------------------------------------------------------------------
run = True
clock = pygame.time.Clock()

PLAYER_RECT = pygame.Rect(PLAYER_LOCATION[0], PLAYER_LOCATION[1], PLAYER.get_width(), PLAYER.get_height())
TEST_RECT = pygame.Rect(100, 100, 100, 50)

while run:
    SCREEN.fill(WHITE)
    
    clock.tick(FPS)

    if PLAYER_LOCATION[1] > SCREEN_HEIGHT - PLAYER.get_height():
        GRAVITY = -GRAVITY
    else:
        GRAVITY += 0.2
    PLAYER_LOCATION[1] += GRAVITY

    if MOVE_RIGHT == True:
        PLAYER_LOCATION[0] += 10
    if MOVE_LEFT == True:
        PLAYER_LOCATION[0] -= 10


    PLAYER_RECT.x = PLAYER_LOCATION[0]
    PLAYER_RECT.y = PLAYER_LOCATION[1]

    if PLAYER_RECT.colliderect(TEST_RECT):
        pygame.draw.rect(SCREEN, (255, 0, 0), TEST_RECT)
    else:
        pygame.draw.rect(SCREEN, (0, 0, 0), TEST_RECT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                MOVE_LEFT = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                MOVE_RIGHT = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                MOVE_LEFT = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                MOVE_RIGHT = False
    
    SCREEN.blit(PLAYER, PLAYER_LOCATION)
    
    pygame.display.flip() # update display
    
pygame.quit()