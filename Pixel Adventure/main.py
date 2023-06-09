import pygame, os, csv



pygame.init()

# Vars -------------------------------------------------------------------
DIR = os.path.dirname(__file__)


WINDOW_SIZE = (1280, 768)
WINDOW_GAME = (640,480)

FPS = 60

SCREEN = pygame.display.set_mode(WINDOW_SIZE)

DISPLAY = pygame.Surface(WINDOW_GAME)

FONT = pygame.font.SysFont("comicsans", 20)


MOVE_RIGHT = False
MOVE_LEFT = False
JUMP = False
FALL = False
#DOUBLE_JUMP = False
GRAVITY = 0

FRAME = 0
FRAME_FRUITS = 0

PLAY_TIMES = 0

QUANTITY_FRUIT = 0
PASS = False

FLIP = False
PLAYER_ACTION = 'idle'
INDEX_SHEET = 11

TILE_SHEET = []

TILE_SIZE = 16

SPRITE_100 = 'Apple.png'
SPRITE_101 = 'Bananas.png'

# Colors -------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BLUE = (146, 244, 255)


# Images --------------------------------------------------------------------

PLAYER_ANIMATION = {}

ANIMATIONS = {"idle": "Idle.png", "run": "Run.png", "jump": "Jump.png", "fall": "Fall.png"}

TERRAIN_SHEET = pygame.image.load(os.path.join(DIR, 'Assets', 'Terrain', 'Terrain (16x16).png'))

# Sounds ---------------------------------------------------------------------

# MAP ---------------------------------------------------------------------

MAP = []

def read_csv(filename):
    map = []
    with open(os.path.join(DIR, 'Maps', filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map

# Functions -------------------------------------------------------------------


# Criando o sistema de animações do personagem
def load_image(filename, index):
    global FRAME
    path = os.path.join(DIR, 'Assets', 'Main Characters', 'Mask Dude', filename)
    
    img_sheet = pygame.image.load(path)

    if FRAME > index:
        FRAME = 0

    player_animation = []
    if filename in ["Idle.png", "Run.png", "Jump.png", "Fall.png"]:
         for i in range(index):
            img = img_sheet.subsurface((i * 32, 0), (32, 32))
            player_animation.append(img)
    return player_animation[int(FRAME)]


# Mudando a animação do Player
def change_action(player_action):
    global INDEX_SHEET, PLAYER_ACTION
    if player_action == 'idle':
        INDEX_SHEET = 11
        PLAYER_ACTION = 'idle'
    if player_action == 'run':
        INDEX_SHEET = 12
        PLAYER_ACTION = 'run'
    if player_action == 'jump':
        INDEX_SHEET = 1
        PLAYER_ACTION = 'jump'
    if player_action == 'fall':
        INDEX_SHEET = 1
        PLAYER_ACTION = 'fall'
    if player_action == 'double_jump':
        INDEX_SHEET = 6
        PLAYER_ACTION = 'double_jump'

def load_terrain():
    list_tile = []
    for y in range(10):
        for x in range(22):
            list_tile.append(TERRAIN_SHEET.subsurface((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)))
    return list_tile 
        

def collision_test(rect, tiles, list_type):
    hit_list = []
    collision_type = 0
    i = 0
    index = 0
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
            collision_type = list_type[i]
            index = i
        i += 1

    return hit_list, collision_type, index

is_collidin_bottom = False

def move(rect, movement, tiles, list_type):
    global QUANTITY_FRUIT, is_collidin_bottom
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    collision_type = 0
    rect.x += movement[0]
    hit_list, collision_type, index = collision_test(rect, tiles, list_type)
    for tile in hit_list:

        if collision_type == '2':
            QUANTITY_FRUIT -= 1

        if movement[0] > 0 and collision_type != '2':
            if collision_type == '1':
                rect.right = tile.left
                collision_types['right'] = True
        elif movement[0] < 0 and collision_type != '2':
            if collision_type == '1':
                rect.left = tile.right
                collision_types['left'] = True

    rect.y += movement[1]
    hit_list, collision_type, index = collision_test(rect, tiles, list_type)

    for tile in hit_list:

        if collision_type == '2':
            QUANTITY_FRUIT -= 1

        if movement[1] > 0 and collision_type != '2':
            print('Colisão Rect Bottom: ', rect.bottom, 'Colisão Tile Top: ', tile.top)
            if rect.bottom -1 == tile.top or rect.bottom +2 == tile.top and collision_type == '3':
                rect.bottom = tile.top
                collision_types['bottom'] = True

            if collision_type == '1':
                rect.bottom = tile.top
                collision_types['bottom'] = True
        elif movement[1] < 0:
            if collision_type == '1':
                rect.top = tile.bottom
                collision_types['top'] = True

    return rect, collision_types

def get_fruits(filename, index):
    global FRAME_FRUITS
    list_fruits = []
    path = os.path.join(DIR, 'Assets', 'Items', 'Fruits', filename)

    img = pygame.image.load(path)

    if FRAME_FRUITS > index:
        FRAME_FRUITS = 0

    if filename in ['Apple.png', 'Bananas.png', 'Cherries.png', 'Kiwi.png', 'Melon.png', 'Orange.png', 'Pineapple.png', 'Strawberry.png', 'Collected.png']:
        for i in range(index):
            list_fruits.append(img.subsurface((i * 32, 0), (32, 32)))
    return list_fruits[int(FRAME_FRUITS)]
    


# Classes ----------------------------------------------------------------------    


PLAYER_RECT = pygame.Rect(100, 100, 23, 32)
FRUIT_RECT = pygame.Rect(100, 18, TILE_SIZE, TILE_SIZE)

run = True
clock = pygame.time.Clock()
air_timer = 0
while run:

    DISPLAY.fill(BLUE)

    MAP = read_csv(os.path.join(DIR, 'Maps', 'lvl_01.csv'))
    TILE_SHEET = load_terrain()

    tile_rect = []
    list_type = []
    for y, layer in enumerate(MAP):
        for x, tile in enumerate(layer):
            tile_value = int(tile)
            if tile_value in [1, 2, 4, 6, 7, 8, 9, 10, 12, 13, 14, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 39, 40, 41, 45, 50, 51, 57, 58]:
                DISPLAY.blit(TILE_SHEET[tile_value], (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '100':
                DISPLAY.blit(get_fruits(SPRITE_100, 17), (x * TILE_SIZE - 16//2, y * TILE_SIZE - 16//2))
                if PASS != True:
                    QUANTITY_FRUIT += 1
            if tile == '101':
                DISPLAY.blit(get_fruits(SPRITE_101, 17), (x * TILE_SIZE - 16//2, y * TILE_SIZE - 16//2))
            if tile != '-1' and tile not in ['39', '40', '41', '100', '101']: # BLocks
                list_type.append('1')
            if tile in ['100', '101']: # Fruits
                list_type.append('2')
            if tile in ['39', '40', '41']: #Plataform
                list_type.append('3')
                #pygame.draw.rect(DISPLAY, WHITE, pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile != '-1':
                tile_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    PASS = True
    # PLAYER STUFFS --------------------------------------------------------------------
    pygame.draw.rect(DISPLAY, WHITE, PLAYER_RECT)

    FRAME_FRUITS += 0.45
    FRAME += 0.45

    PLAYER_ANIMATION = load_image(ANIMATIONS[PLAYER_ACTION], INDEX_SHEET)

    DISPLAY.blit(pygame.transform.flip(PLAYER_ANIMATION, FLIP, False), (PLAYER_RECT.x - 3.5, PLAYER_RECT.y))

    # DISPLAY.blit(get_fruits("Apple.png", 17), (FRUIT_RECT.x - 16//2, FRUIT_RECT.y - 16//2))
    
    player_movement = [0, 0]
    
    if MOVE_RIGHT:
        player_movement[0] += 2
        #PLAYER_RECT.x += 2
    if MOVE_LEFT:
        player_movement[0] -= 2
        #PLAYER_RECT.x -= 2

    player_movement[1] += GRAVITY

    GRAVITY += 0.2
    

    if player_movement[0] > 0 and JUMP == False and FALL == False:
        change_action('run')
        FLIP = False
    if player_movement[0] == 0 and JUMP == False and FALL == False:
        change_action('idle')
    if player_movement[0] < 0 and JUMP == False and FALL == False:
        change_action('run')
        FLIP = True

    if JUMP == True:
        change_action('jump')
        if player_movement[0] < 0:
            FLIP = True
        if player_movement[0] > 0:
            FLIP = False
    if FALL == True:
        change_action('fall')
        if player_movement[0] < 0:
            FLIP = True
        if player_movement[0] > 0:
            FLIP = False

    PLAYER_RECT, collisions = move(PLAYER_RECT, player_movement, tile_rect, list_type)

    if collisions['bottom']:
        GRAVITY = 0
        air_timer = 0
        FALL = False
        JUMP = False
    if collisions['top']:
        GRAVITY = 0
    else:
        air_timer += 1

    if air_timer >= 30:
        JUMP = False
        FALL = True
    if GRAVITY > 1:
        FALL = True
    #player_movement[1] += GRAVITY

    #GRAVITY += 0.2
    #if GRAVITY > 3:
#        GRAVITY = 3


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_d:
                MOVE_RIGHT = True
            if event.key == pygame.K_a:
                MOVE_LEFT = True
            if event.key == pygame.K_SPACE:
                JUMP = True
                if air_timer < 6:
                    GRAVITY = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                MOVE_RIGHT = False
            if event.key == pygame.K_a:
                MOVE_LEFT = False

    text_quantity_fruit = FONT.render(str(QUANTITY_FRUIT), False, WHITE)
    DISPLAY.blit(text_quantity_fruit, (120, 20))
    DISPLAY.blit(get_fruits("Apple.png", 17), (FRUIT_RECT.x - 8, FRUIT_RECT.y - 8))

    text = FONT.render(str(round(clock.get_fps(),2)), True, WHITE)

    DISPLAY.blit(text,(640 - 100, 20))

    SCREEN.blit(pygame.transform.scale(DISPLAY, WINDOW_SIZE), (0, 0))
    pygame.display.flip() # update display
    clock.tick(FPS)