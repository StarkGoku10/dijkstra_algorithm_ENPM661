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
BORDER_COLOR = (6, 3, 141)  # Change border color
GRAY = (200, 200, 200)
ORANGE = (255, 103, 31)
# Define padding
padding = 5

# Processing
# Original figures without border
big_rectangle = pygame.Rect(5, 5, 1190, 490)
rectangle1 = pygame.Rect(100, 0, 75, 400)
rectangle2 = pygame.Rect(275, 100, 75, 400)

# inverted c shaped figure
rectangle3 = pygame.Rect(1020, 50, 80, 400)
rectangle4 = pygame.Rect(900, 50, 200, 75)
rectangle5 = pygame.Rect(900, 375, 200, 75)

# Create rectangles for border
border_rectangle1 = pygame.Rect(rectangle1.left - padding, rectangle1.top - padding, rectangle1.width + 2 * padding, rectangle1.height + 2 * padding)
border_rectangle2 = pygame.Rect(rectangle2.left - padding, rectangle2.top - padding, rectangle2.width + 2 * padding, rectangle2.height + 2 * padding)
border_rectangle3 = pygame.Rect(rectangle3.left - padding, rectangle3.top - padding, rectangle3.width + 2 * padding, rectangle3.height + 2 * padding)
border_rectangle4 = pygame.Rect(rectangle4.left - padding, rectangle4.top - padding, rectangle4.width + 2 * padding, rectangle4.height + 2 * padding)
border_rectangle5 = pygame.Rect(rectangle5.left - padding, rectangle5.top - padding, rectangle5.width + 2 * padding, rectangle5.height + 2 * padding)


# Calculate hexagon vertices
x_center, y_center = 650, 250
vertex_length = 150
hexagon_vertices = []
for i in range(6):
    angle_rad = math.radians(60 * i-90)
    x = x_center + vertex_length * math.cos(angle_rad)
    y = y_center + vertex_length * math.sin(angle_rad)
    hexagon_vertices.append((x,y))

# Create hexagon border vertices
hexagon_border_vertices = []
for i in range(6):
    angle_rad = math.radians(60 * i-90)
    x = x_center + (vertex_length + padding) * math.cos(angle_rad)  # Add padding to the radius
    y = y_center + (vertex_length + padding) * math.sin(angle_rad)
    hexagon_border_vertices.append((x, y))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(BORDER_COLOR)

    # Draw big background rectangle
    pygame.draw.rect(screen, WHITE, big_rectangle)

    # Draw border rectangles
    pygame.draw.rect(screen, BORDER_COLOR, border_rectangle1)
    pygame.draw.rect(screen, BORDER_COLOR, border_rectangle2)
    pygame.draw.rect(screen, BORDER_COLOR, border_rectangle3)
    pygame.draw.rect(screen, BORDER_COLOR, border_rectangle4)
    pygame.draw.rect(screen, BORDER_COLOR, border_rectangle5)

    # Draw rectangles
    pygame.draw.rect(screen, ORANGE, rectangle1)
    pygame.draw.rect(screen, ORANGE, rectangle2)
    pygame.draw.rect(screen, ORANGE, rectangle3)
    pygame.draw.rect(screen, ORANGE, rectangle4)
    pygame.draw.rect(screen, ORANGE, rectangle5)

    # Draw hexagon border
    pygame.draw.polygon(screen, BORDER_COLOR, hexagon_border_vertices)

    # Draw hexagon
    pygame.draw.polygon(screen, ORANGE, hexagon_vertices)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


