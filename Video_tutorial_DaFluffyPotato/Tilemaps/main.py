import pygame
import os

pygame.init()

# Sound ------------------------------------------------------------------

# Variaveis ------------------------------------------------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60

# Player movement
MOVE_RIGHT = False
MOVE_LEFT = False
GRAVITY = 0


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Template Pygame init")

DISPLAY = pygame.Surface((300, 200))

# Color ------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)





# Images ------------------------------------------------------------------
PLAYER = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'player.png')).convert()

PLAYER.set_colorkey(WHITE)

GRASS_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'grass.png')).convert()

DIRT_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'dirt.png')).convert()

TILE_SIZE = GRASS_IMG.get_width()

# Map ----------------------------------------------------------------------

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['1','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]


MAP_WIDTH = len(game_map[0]) * TILE_SIZE
MAP_HEIGHT = len(game_map) * TILE_SIZE

# Calculate the offset required to center the map
OFFSET_X = (300 - MAP_WIDTH) // 2
OFFSET_Y = (200 - MAP_HEIGHT) // 2

# Funções ------------------------------------------------------------------

def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
# Class ------------------------------------------------------------------


# Main ------------------------------------------------------------------
run = True
clock = pygame.time.Clock()

PLAYER_RECT = pygame.Rect(50, 50, PLAYER.get_width(), PLAYER.get_height())

air_timer = 0

while run:
    DISPLAY.fill(WHITE)
    
    clock.tick(FPS)

    tile_rect = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == '1':
                DISPLAY.blit(DIRT_IMG, (x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y))
            if tile == '2':
                DISPLAY.blit(GRASS_IMG, (x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * TILE_SIZE + OFFSET_X, y * TILE_SIZE + OFFSET_Y, TILE_SIZE, TILE_SIZE))

    
    

    player_movement = [0, 0]
    if MOVE_RIGHT:
        player_movement[0] += 2
        PLAYER = pygame.transform.rotate(PLAYER, 0)
    if MOVE_LEFT:
        player_movement[0] -= 2
        PLAYER = pygame.transform.rotate(PLAYER, -180)
    player_movement[1] += GRAVITY
    GRAVITY += 0.2
    if GRAVITY > 3:
        GRAVITY = 3
    
    PLAYER_RECT, collisions = move(PLAYER_RECT, player_movement, tile_rect)

    if collisions['bottom']:
        GRAVITY = 0
        air_timer = 0
    else:
        air_timer += 1

    DISPLAY.blit(PLAYER, (PLAYER_RECT.x, PLAYER_RECT.y))

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
            if event.key == pygame.K_SPACE:
                if air_timer < 6:
                    GRAVITY = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                MOVE_LEFT = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                MOVE_RIGHT = False
        

    surf = pygame.transform.scale(DISPLAY, (SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.blit(surf, (0, 0))
    pygame.display.flip() # update display
    
pygame.quit()