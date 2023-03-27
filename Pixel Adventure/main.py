import pygame, os, random


pygame.init()

# Vars -------------------------------------------------------------------

WINDOW_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

DIR = os.path.dirname(__file__)

MOVE_RIGHT = False
MOVE_LEFT = False
MOVE_UP = False
MOVE_DOWN = False
GRAVITY = 0

INDEX = 0

# Colors -------------------------------------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (124,252,0)
BLUE = (146, 244, 255)


# Images --------------------------------------------------------------------
# PLAYER_SHEET = pygame.image.load(os.path.join(DIR, 'Assets', 'Main Characters', 'Mask Dude'))

PLAYER_ANIMATION = {}

ANIMATIONS = {"idle": "Idle.png", "run": "Run.png", "jump": "Jump.png", "fall": "Fall.png"}

# Sounds ---------------------------------------------------------------------



# Functions -------------------------------------------------------------------

def load_image(filename, index, frame):
    path = os.path.join(DIR, 'Assets', 'Main Characters', 'Mask Dude', filename)
    
    img_sheet = pygame.image.load(path)

    player_animation = []
    if filename == "Idle.png":
        for i in range(index):
            img = img_sheet.subsurface((i * 32, 0), (32, 32))
            player_animation.append(img)
    if filename == "Run.png":
        for i in range(index):
            img = img_sheet.subsurface((i * 32, 0), (32, 32))
            player_animation.append(img)
    return player_animation

    
# Classes ----------------------------------------------------------------------


PLAYER_RECT = pygame.Rect(100, 100, 50, 50)

run = True

while run:

    SCREEN.fill(WHITE)
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

    player_movement = [0, 0]

    pygame.draw.rect(SCREEN,GREEN, PLAYER_RECT)



    PLAYER_ANIMATION = load_image(ANIMATIONS["idle"], 11)

    

    if MOVE_RIGHT:
        #player_movement[0] += 2
        PLAYER_RECT.x += 2
    if MOVE_LEFT:
        #player_movement[0] -= 2
        PLAYER_RECT.x -= 2
    if MOVE_UP:
       # player_movement[1] -= 2
        PLAYER_RECT.y -= 2
    if MOVE_DOWN:
       # player_movement[1] += 2
        PLAYER_RECT.y += 2

    #player_movement[1] += GRAVITY

    #GRAVITY += 0.2
    #if GRAVITY > 3:
#        GRAVITY = 3



    pygame.display.flip()