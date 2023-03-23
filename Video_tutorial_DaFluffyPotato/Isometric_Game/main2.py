import pygame
import random

# initialize pygame
pygame.init()

# set the screen dimensions
screen_width = 640
screen_height = 480

# set the tile size
tile_size = 32

# set the number of tiles in the world
world_width = 20
world_height = 20

# create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# set the background color
background_color = (255, 255, 255)

# define the colors for the tiles
grass_color = (34, 177, 76)
water_color = (63, 72, 204)
sand_color = (237, 201, 175)

# define the tiles for the world
world = [[None] * world_height for i in range(world_width)]
for x in range(world_width):
    for y in range(world_height):
        r = random.randint(1, 100)
        if r < 50:
            world[x][y] = "grass"
        elif r < 80:
            world[x][y] = "water"
        else:
            world[x][y] = "sand"

# define a function to draw the isometric grid
def draw_grid():
    for x in range(world_width):
        for y in range(world_height):
            if world[x][y] == "grass":
                rect_color = grass_color
            elif world[x][y] == "water":
                rect_color = water_color
            elif world[x][y] == "sand":
                rect_color = sand_color
            rect = pygame.Rect(x * tile_size + (y * tile_size) / 2, y * tile_size / 2, tile_size, tile_size)
            pygame.draw.rect(screen, rect_color, rect)

# define the main game loop
def main():
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # clear the screen
        screen.fill(background_color)

        # draw the isometric grid
        draw_grid()

        # update the display
        pygame.display.update()

# start the game loop
if __name__ == "__main__":
    main()