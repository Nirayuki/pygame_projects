import pygame
import os

pygame.init()

# Sound ------------------------------------------------------------------

# Variaveis ------------------------------------------------------------------
WINDOW_SIZE = (1280,720)
FPS = 60

# Player movement
MOVE_RIGHT = False
MOVE_LEFT = False
GRAVITY = 0


SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0 ,32)
pygame.display.set_caption("Template Pygame init")

DISPLAY = pygame.Surface((300, 200))

# Color ------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BLUE = (146, 244, 255)




# Images ------------------------------------------------------------------
PLAYER = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'player.png')).convert()

PLAYER.set_colorkey(WHITE)

GRASS_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'grass.png')).convert()

DIRT_IMG = pygame.image.load(os.path.join(os.path.dirname(__file__), 'Assets', 'dirt.png')).convert()

TILE_SIZE = GRASS_IMG.get_width()

# Map ----------------------------------------------------------------------

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map



game_map = load_map(os.path.join(os.path.dirname(__file__), 'map'))

TRUE_SCROLL = [0, 0]

# Aqui eu to criando diversos tipo de objetos, o primeiro valor é o valor do parallax, e o outro valor é o valor do X, Y, tamanho do rect.
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

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

PLAYER_RECT = pygame.Rect(100,100,5,13)

air_timer = 0

while run:
    DISPLAY.fill(BLUE)
    


    # Câmera para seguir o player, o conceito de câmera é basicamente dar um SCROLL para todos os assets, ou seja, fazer eles andarem para fora da tela.
    TRUE_SCROLL[0] += (PLAYER_RECT.x - TRUE_SCROLL[0] - 152)/20
    TRUE_SCROLL[1] += (PLAYER_RECT.y - TRUE_SCROLL[1] - 106)/20

    SCROLL = TRUE_SCROLL.copy()
    SCROLL[0] = int(SCROLL[0])
    SCROLL[1] = int(SCROLL[1])


    # Criando um rect aleatório no meio da tela com cor verde
    pygame.draw.rect(DISPLAY, GREEN, pygame.Rect(0, 120, 300, 80))

    # Aqui eu to passando por todos os objetos e criando um rect com cada uma das informações, a multiplicação serve para saber qual vai ser q velocidade do parallax de cada um.
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - SCROLL[0] * background_object[0], background_object[1][1] - SCROLL[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(DISPLAY,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(DISPLAY,(9,91,85),obj_rect)


    tile_rect = []
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile == '1':
                DISPLAY.blit(DIRT_IMG, (x * TILE_SIZE - SCROLL[0], y * TILE_SIZE - SCROLL[1]))
            if tile == '2':
                DISPLAY.blit(GRASS_IMG, (x * TILE_SIZE -  SCROLL[0], y * TILE_SIZE - SCROLL[1]))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    
    

    player_movement = [0, 0]
    if MOVE_RIGHT:
        player_movement[0] += 2
    if MOVE_LEFT:
        player_movement[0] -= 2
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

    DISPLAY.blit(PLAYER, (PLAYER_RECT.x - SCROLL[0], PLAYER_RECT.y - SCROLL[1]))

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
        

    SCREEN.blit(pygame.transform.scale(DISPLAY, WINDOW_SIZE), (0, 0))
    pygame.display.flip() # update display
    clock.tick(FPS)
    
pygame.quit()