import cv2
import numpy as np


map_width = 500
map_height = 1200

NAVY_COLOR = (141, 3, 6)
# Create a blank white image
image = np.ones((map_width, map_height, 3), dtype=np.uint8) * 255

# Draw black border around the map
border_thickness = 5
cv2.rectangle(image, (0, 0), (map_height - 1, map_width - 1), (141, 3, 6), border_thickness)

polygon_sides = 6
polygon_length = 150
polygon_bloat = 5
PADDING_COLOR = (31,103,255)
padding = 5

# Draw rectangles
cv2.rectangle(image, (100 - padding, -50 - padding), (175 + padding, 350 + padding), NAVY_COLOR, -1)
cv2.rectangle(image, (275 - padding, 100 - padding), (350 + padding, 500 + padding), NAVY_COLOR, -1)

cv2.rectangle(image, (100, -50), (175, 350), PADDING_COLOR, -1)
cv2.rectangle(image, (275, 100), (350, 500), PADDING_COLOR, -1)

# Calculate the vertices of the polygon
polygon_vertices = []
for i in range(polygon_sides):
    angle = np.radians(i * (360 / polygon_sides) + 90)
    x = 650 + ((polygon_length + polygon_bloat) - padding) * np.cos(angle)
    y = 250 + ((polygon_length + polygon_bloat) - padding) * np.sin(angle)
    polygon_vertices.append((int(x), int(y)))

# Draw the polygon
cv2.fillPoly(image, [np.array(polygon_vertices)], PADDING_COLOR)
cv2.polylines(image, [np.array(polygon_vertices)], isClosed=True, color=NAVY_COLOR, thickness=5)

# Draw U-shaped rectangle
cv2.rectangle(image, (1020 - padding, 50 - padding), (1100 + padding, 450 + padding), NAVY_COLOR, -1)  # Right vertical part of U
cv2.rectangle(image, (900 - padding, 50 - padding), (1100 + padding, 125 + padding), NAVY_COLOR, -1)  # Top vertical part of U
cv2.rectangle(image, (900 - padding, 375 - padding), (1100 + padding, 450 + padding), NAVY_COLOR, -1)  # Bottom Horizontal part of U

# Draw padding for U-shaped rectangle
cv2.rectangle(image, (1020, 50), (1100, 450), PADDING_COLOR, -1)  # Right vertical part of U without padding
cv2.rectangle(image, (900, 50), (1100, 125), PADDING_COLOR, -1 )  # Top vertical part of U without padding
cv2.rectangle(image, (900, 375), (1100, 450), PADDING_COLOR, -1)  # Bottom Horizontal part of U without padding

# Display the image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
