import pygame
import os
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)


# Variaveis ------------------------------------------------------------------
WINDOW_SIZE = (1280,720)
FPS = 60

# Player movement
MOVE_RIGHT = False
MOVE_LEFT = False
GRAVITY = 0


# Chunck
CHUNCK_SIZE = 8

SCREEN = pygame.display.set_mode(WINDOW_SIZE, 0 ,32)
pygame.display.set_caption("Template Pygame init")

DISPLAY = pygame.Surface((300, 200))

# Color ------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BLUE = (146, 244, 255)




# Images ------------------------------------------------------------------
DIR = os.path.dirname(__file__)

# PLAYER = pygame.image.load(os.path.join(DIR, 'Assets', 'player.png')).convert()

# PLAYER.set_colorkey(WHITE)

GRASS_IMG = pygame.image.load(os.path.join(DIR, 'Assets', 'grass.png')).convert()

DIRT_IMG = pygame.image.load(os.path.join(DIR, 'Assets', 'dirt.png')).convert()

PLANT_IMG = pygame.image.load(os.path.join(DIR, 'Assets', 'plant.png')).convert()
PLANT_IMG.set_colorkey(WHITE)

TILE_SIZE = GRASS_IMG.get_width()
TILE_INDEX = {1:GRASS_IMG, 2:DIRT_IMG, 3:PLANT_IMG}

# Sound ------------------------------------------------------------------

JUMP_SOUND = pygame.mixer.Sound(os.path.join(DIR, 'Sounds', 'jump.wav'))

GRASS_SOND = [pygame.mixer.Sound(os.path.join(DIR, 'Sounds', 'grass_0.wav')), pygame.mixer.Sound(os.path.join(DIR, 'Sounds', 'grass_1.wav'))]
GRASS_SOND[0].set_volume(0.2)
GRASS_SOND[1].set_volume(0.2)

pygame.mixer.music.load(os.path.join(DIR, 'Sounds', 'music.wav'))
pygame.mixer.music.play(-1)

GRASS_SOUND_TIMER = 0

# Funções ------------------------------------------------------------------

# Nessa funçào eu estou criando chunks e gerando um mapa para cada um. É a mesma ideia do minecraft.

def generate_chuncks(x, y):
    chunck_data = []
    for y_pos in range(CHUNCK_SIZE):
        for x_pos in range(CHUNCK_SIZE):
            target_x = x * CHUNCK_SIZE + x_pos
            target_y = y * CHUNCK_SIZE + y_pos
            tile_type = 0 # Nothing
            if target_y > 10:
                tile_type = 2 # Dirt.png
            elif target_y == 10:
                tile_type = 1 # Glass.png
            elif target_y == 9:
                if random.randint(1, 5) == 1:
                    tile_type = 3 # Plant.png
            if tile_type != 0:
                chunck_data.append([[target_x, target_y], tile_type])
    return chunck_data

global animation_frames
animation_frames = {}

def load_animation(path, frame_duration):

    # Achando o caminho da imagem, no frame_duration a gente consegue saber quantas vezes será mostrado essa imagem.
    global animation_frames
    print(path.split('/') [-1])
    animation_name = path.split('/') [-1]
    animation_frame_data = []

    # Pegando a imagem e colocando no animation_frame_data.
    for n, frame in enumerate(frame_duration):
        animation_frame_id = animation_name + '_' + str(n)
        img_location = path + '/' + animation_frame_id + '.png'
        animaiton_image = pygame.image.load(img_location).convert()
        animaiton_image.set_colorkey(WHITE)
        animation_frames[animation_frame_id] = animaiton_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
    return animation_frame_data

# Essa função indentifica que você mudou de animação.
def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

animation_database = {}

animation_database['run'] = load_animation((os.path.join(DIR, 'Assets', 'run')), [7, 7]) # 2 valores pq são 2 imagens | Esses valores são os frames
animation_database['idle'] = load_animation((os.path.join(DIR, 'Assets', 'idle')), [7, 7, 40]) # 3 valores pq são 4 imagens | Esses valores são os frames


player_action = 'idle'
player_frame = 0
player_flip = False

# print(load_animation((os.path.join(DIR, 'Assets', 'idle')), [7, 7, 40]))

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


# Map ----------------------------------------------------------------------

# game_map = load_map(os.path.join(DIR, 'map'))
game_map = {}

TRUE_SCROLL = [0, 0]

# Aqui eu to criando diversos tipo de objetos, o primeiro valor é o valor do parallax, e o outro valor é o valor do X, Y, tamanho do rect.
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

# Class ------------------------------------------------------------------


# Main ------------------------------------------------------------------
run = True
clock = pygame.time.Clock()

PLAYER_RECT = pygame.Rect(100,100,5,13)

air_timer = 0

while run:
    DISPLAY.fill(BLUE)
    
    if GRASS_SOUND_TIMER > 0:
        GRASS_SOUND_TIMER -= 1

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

    # Tile rendering
    for y in range(3):
        for x in range(4):
            target_x = x  - 1 + int(round(SCROLL[0] / (CHUNCK_SIZE * TILE_SIZE)))
            target_y = y - 1 + int(round(SCROLL[1] / (CHUNCK_SIZE * TILE_SIZE)))
            target_chunk = str(target_x) + ';' + str(target_y)
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chuncks(target_x, target_y)
            for tile in game_map[target_chunk]:
                DISPLAY.blit(TILE_INDEX[tile[1]], (tile[0][0] * TILE_SIZE - SCROLL[0], tile[0][1] * TILE_SIZE - SCROLL[1]))
                if tile[1] in [1, 2]:
                    tile_rect.append(pygame.Rect(tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    

    player_movement = [0, 0]

    if MOVE_RIGHT:
        player_movement[0] += 2

    if MOVE_LEFT:
        player_movement[0] -= 2

    player_movement[1] += GRAVITY

    GRAVITY += 0.2
    if GRAVITY > 3:
        GRAVITY = 3

    # Verificando a movimentação do player e colocando as animações
    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    
    PLAYER_RECT, collisions = move(PLAYER_RECT, player_movement, tile_rect)

    if collisions['bottom']:
        GRAVITY = 0
        air_timer = 0
        if player_movement[0] != 0:
            if GRASS_SOUND_TIMER == 0:
                GRASS_SOUND_TIMER = 50
                random.choice(GRASS_SOND).play()
    else:
        air_timer += 1

    player_frame += 1
    # Verificando se a animação acabou e setando o frame para 0 fazendo um loop
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    # Procurando no banco de dados de animeções, o nome da animaçào se é Run or Idle e depois o frame especifico dela
    player_img_id = animation_database[player_action][player_frame]
    PLAYER = animation_frames[player_img_id]
    DISPLAY.blit(pygame.transform.flip(PLAYER, player_flip, False), (PLAYER_RECT.x - SCROLL[0], PLAYER_RECT.y - SCROLL[1]))

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
                    JUMP_SOUND.play()
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