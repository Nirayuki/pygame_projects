import pygame, os, csv



pygame.init()

# Vars -------------------------------------------------------------------
DIR = os.path.dirname(__file__)


WINDOW_SIZE = (1280, 768)
WINDOW_GAME = (640,480)

FPS = 60

SCREEN = pygame.display.set_mode(WINDOW_SIZE)

DISPLAY = pygame.Surface(WINDOW_GAME)



MOVE_RIGHT = False
MOVE_LEFT = False
MOVE_UP = False
MOVE_DOWN = False
GRAVITY = 0

FRAME = 0

FLIP = False
PLAYER_ACTION = 'idle'
INDEX_SHEET = 11

TILE_SHEET = []

TILE_SIZE = 16

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

def load_map(filename):
    tiles = []
    map = read_csv(filename)

    for x, row in enumerate(map):
        for tile in row:
            pass
# Functions -------------------------------------------------------------------


# Criando o sistema de animações do personagem
def load_image(filename, index, frame):
    global FRAME
    path = os.path.join(DIR, 'Assets', 'Main Characters', 'Mask Dude', filename)
    
    img_sheet = pygame.image.load(path)

    if FRAME > index:
        FRAME = 0

    player_animation = []
    if filename == "Idle.png":
        for i in range(index):
            img = img_sheet.subsurface((i * 32, 0), (32, 32))
            player_animation.append(img)
    if filename == "Run.png":
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
        for x in range(21):
            list_tile.append(TERRAIN_SHEET.subsurface((x * 16, y * 16), (16, 16)))
    return list_tile 
        
# Classes ----------------------------------------------------------------------


PLAYER_RECT = pygame.Rect(100, 100, 32, 32)

run = True
clock = pygame.time.Clock()

while run:

    DISPLAY.fill(WHITE)
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
            if event.key == pygame.K_w:
                MOVE_UP = True
            if event.key == pygame.K_s:
                MOVE_DOWN = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                MOVE_RIGHT = False
            if event.key == pygame.K_a:
                MOVE_LEFT = False
            if event.key == pygame.K_w:
                MOVE_UP = False
            if event.key == pygame.K_s:
                MOVE_DOWN = False

    FRAME += 0.45

    PLAYER_ANIMATION = load_image(ANIMATIONS[PLAYER_ACTION], INDEX_SHEET, int(FRAME))

    DISPLAY.blit(pygame.transform.flip(PLAYER_ANIMATION, FLIP, False), (PLAYER_RECT.x, PLAYER_RECT.y))
    
    player_movement = [0, 0]
    
    if MOVE_RIGHT:
        player_movement[0] += 2
        PLAYER_RECT.x += 2
    if MOVE_LEFT:
        player_movement[0] -= 2
        PLAYER_RECT.x -= 2
    if MOVE_UP:
        player_movement[1] -= 2
        PLAYER_RECT.y -= 2
    if MOVE_DOWN:
        player_movement[1] += 2
        PLAYER_RECT.y += 2

    if player_movement[0] > 0:
        change_action('run')
        FLIP = False
    if player_movement[0] == 0:
        change_action('idle')
    if player_movement[0] < 0:
        change_action('run')
        FLIP = True

    MAP = read_csv(os.path.join(DIR, 'Maps', 'lvl_01.csv'))
    TILE_SHEET = load_terrain()

    tile_rect = []
    for y, layer in enumerate(MAP):
        for x, tile in enumerate(layer):
            if tile == '1':
                DISPLAY.blit(TILE_SHEET[1], (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                DISPLAY.blit(TILE_SHEET[2], (x * TILE_SIZE, y * TILE_SIZE ))
            if tile == '6':
                DISPLAY.blit(TILE_SHEET[6], (x * TILE_SIZE, y * TILE_SIZE ))
            if tile == '7':
                DISPLAY.blit(TILE_SHEET[7], (x * TILE_SIZE, y * TILE_SIZE ))
            if tile == '23':
                DISPLAY.blit(TILE_SHEET[23], (x * TILE_SIZE, y * TILE_SIZE ))
            if tile != '0':
                tile_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    #terrain = TERRAIN_SHEET.subsurface((0 * 16, 10 * 16), (16, 16))
    #DISPLAY.blit(terrain, (50, 50))

    #player_movement[1] += GRAVITY

    #GRAVITY += 0.2
    #if GRAVITY > 3:
#        GRAVITY = 3



    SCREEN.blit(pygame.transform.scale(DISPLAY, WINDOW_SIZE), (0, 0))
    pygame.display.flip() # update display
    clock.tick(FPS)