import pygame, os, random


pygame.init()

# Vars -------------------------------------------------------------------

WINDOW_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

# Colors -------------------------------------------------------------------

WHITE = (255, 255, 255)


# Images --------------------------------------------------------------------


# Sounds --------------------------------------------------------------------

# Functions -------------------------------------------------------------------



# Classes ----------------------------------------------------------------------


run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    SCREEN.fill(WHITE)
    pygame.display.flip()