import pygame
import sys
import math 

# Initialize Pygame
pygame.init()

# Set up the screen
width1, height1 = 1200, 500
screen = pygame.display.set_mode((width1, height1))
pygame.display.set_caption("Draw Rectangles")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Processing
rectangle1 = pygame.Rect(100, 0, 75, 400)
rectangle2 = pygame.Rect(275, 100, 75, 400)

# inverted c shaped figure
rectangle3 = pygame.Rect(1020, 50, 80, 400)
rectangle4 = pygame.Rect(900, 50, 200, 75)
rectangle5 = pygame.Rect(900, 375, 200, 75)

x_center, y_center = 650, 250
vertex_length = 150
hexagon_vertices = []
for i in range(6):
    angle_rad = math.radians(60 * i)
    x = x_center + vertex_length * math.cos(angle_rad)
    y = y_center + vertex_length * math.sin(angle_rad)
    hexagon_vertices.append((x,y))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(WHITE)

    # Draw rectangles
    pygame.draw.rect(screen, BLACK, rectangle1)
    pygame.draw.rect(screen, BLACK, rectangle2)
    pygame.draw.rect(screen, BLACK, rectangle3)
    pygame.draw.rect(screen, BLACK, rectangle4)
    pygame.draw.rect(screen, BLACK, rectangle5)
    # pygame.draw.rect(screen, RED, rectangle3)
    pygame.draw.polygon(screen, BLACK, hexagon_vertices)
    

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


