import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the caption
pygame.display.set_caption("Isometric Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set the tile size
TILE_WIDTH = 32
TILE_HEIGHT = 16

# Load images
player_image = pygame.image.load("player.png").convert_alpha()
tree_image = pygame.image.load("tree.png").convert_alpha()

# Define the Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        screen.blit(player_image, (self.x, self.y))
        
# Define the Tree class
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        screen.blit(tree_image, (self.x, self.y))

# Define a function to draw the isometric grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, TILE_WIDTH):
        for y in range(0, SCREEN_HEIGHT, TILE_HEIGHT):
            rect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
            pygame.draw.rect(screen, WHITE, rect, 1)

# Define the main game loop
def main():
    # Create the player
    player = Player(400, 300)
    
    # Create some trees
    trees = []
    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH - TILE_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - TILE_HEIGHT)
        tree = Tree(x, y)
        trees.append(tree)
    
    # Start the game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the isometric grid
        draw_grid()
        
        # Draw the trees
        for tree in trees:
            tree.draw()
        
        # Draw the player
        player.draw()
        
        # Update the display
        pygame.display.update()

# Start the game
if __name__ == "__main__":
    main()