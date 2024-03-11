###################################### Repository link ##############################################
########### https://github.com/StarkGoku10/dijkstra_algorithm_ENPM661.git ###########################
#####################################################################################################


import numpy as np
import math
import cv2
import time
from queue import PriorityQueue

# defining the search space(map)
map_width = 1200
map_height = 500

#mapping the obstacle space, 
hexagon_sides = 6
hexagon_vertex_len = 150
BORDER_COLOR = (141, 31, 6)
OBS_COLOR = (31, 103, 255)
border = 5  #thickness of the clearance 

# Creating the background for search map
image = np.ones((map_height, map_width, 3), dtype=np.uint8) * 255

# Drawing border around the map
border_thickness = 5
cv2.rectangle(image, (0, map_height - 1), (map_width - 1, 0), BORDER_COLOR, border_thickness)

# Drawing the rectangles with border 
cv2.rectangle(image, (100 - border, 0 - border), (175 + border, 400 + border), BORDER_COLOR, -1)
cv2.rectangle(image, (100, 0), (175, 400), OBS_COLOR, -1)
cv2.rectangle(image, (275 - border, map_height - 400 - border), (350 + border, map_height + border), BORDER_COLOR, -1)
cv2.rectangle(image, (275, map_height - 400), (350, map_height), OBS_COLOR, -1)

# Plotting the vertices of the hexagon with border
hexagon_vertices = []
for i in range(hexagon_sides):
    angle = np.radians(i * (360 / hexagon_sides) + 90)
    x = 650 + ((hexagon_vertex_len) * np.cos(angle))
    y = map_height - (250 + ((hexagon_vertex_len) * np.sin(angle)))
    hexagon_vertices.append((int(x), int(y)))

# Draw the hexagon
cv2.fillPoly(image, [np.array(hexagon_vertices)], OBS_COLOR)
cv2.polylines(image, [np.array(hexagon_vertices)], isClosed=True, color=(141, 31, 6), thickness=5)

# Drawing the inverted C-shaped rectangle with border
cv2.rectangle(image, (1020 - border, map_height - 50 + border), (1100 + border, map_height - 450 - border), BORDER_COLOR, -1)  
cv2.rectangle(image, (1020, map_height - 50), (1100, map_height - 450), OBS_COLOR, -1)
cv2.rectangle(image, (900 - border, map_height - 50 + border), (1100 + border, map_height - 125 - border), BORDER_COLOR, -1)  
cv2.rectangle(image, (900, map_height - 50), (1100, map_height - 125), OBS_COLOR, -1)
cv2.rectangle(image, (900 - border, map_height - 375 + border), (1100 + border, map_height - 450 - border), BORDER_COLOR, -1)  
cv2.rectangle(image, (900, map_height - 375), (1100, map_height - 450), OBS_COLOR, -1)


map_width = 1200
map_height = 500

# Defining a node class to store the coordinates, cost and the index of the parent node.

class Node:
    def __init__(self, x, y, cost, parent_id):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent_id = parent_id

    def __lt__(self, other):
        return self.cost < other.cost

# Configuring the obstacle space and constructing the obstacles
def Configuration_space(image):
    obs_space = np.zeros((map_height, map_width), dtype=np.uint8)
    for y in range(map_height):
        for x in range(map_width):
            if np.all(image[y, x] == BORDER_COLOR) or np.all(image[y, x] == OBS_COLOR) or x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1:
                obs_space[y, x] = 255
    return obs_space



 # Check if coordinates are within the boundaries of the obstacle space and if the cell is occupied by an obstacle (value 255)
def Validity(x, y, obs_space):
    if x < 0 or x >= map_width or y < 0 or y >= map_height or obs_space[y][x] == 255:
        return False
    return True


# checking if the goal node is reached or not
def Check_goal(present, goal):
    return present.x == goal.x and present.y == goal.y


# generating a unique key for each node 
def key(node):
    return 1022 * node.x + 111 * node.y

# generate child nodes
def up(x, y, cost):
    return x, y - 1, cost + 1

def up_right(x, y, cost):
    return x + 1, y + 1, cost + 1.414

def right(x, y, cost):
    return x + 1, y, cost + 1

def bottom_right(x, y, cost):
    return x + 1, y - 1, cost + 1.414

def down(x, y, cost):
    return x, y + 1, cost + 1

def bottom_left(x, y, cost):
    return x - 1, y - 1, cost + 1.414

def left(x, y, cost):
    return x - 1, y, cost + 1

def up_left(x, y, cost):
    return x - 1, y + 1, cost + 1.414


# implementing the djisktra algorithm 
def dijkstra(start, goal, obs_space):
    start_time = time.time()  # Starting the clock count to calculate the time taken to reach goal node
    if not Validity(start.x, start.y, obs_space):
        print("Invalid start node")
        return None, 0, 0

    if not Validity(goal.x, goal.y, obs_space):
        print("Invalid goal node")
        return None, 0, 0

    if Check_goal(start, goal):
        return None, 1, 0

    goal_node = goal
    start_node = start

    moves = [up, down, left, right, bottom_left, bottom_right, up_left, up_right]
    # Dictionary to store unexplored nodes
    unexplored_nodes = {}  

   # Generating a unique key for identifying the node
    start_key = key(start_node)  
    unexplored_nodes[start_key] = start_node

    # Set to store explored nodes
    explored_nodes = set()  
    # Priority queue for storing nodes based on their cost
    priority_queue = PriorityQueue()  

    # Add start node to the priority queue
    priority_queue.put((start_node.cost, start_node))  

    # stores all nodes that have been traversed, for visualization purposes.
    all_nodes = []  

    while not priority_queue.empty():
        # Popping the first element in the priority queue to create child nodes for exploration
        cost, present_node = priority_queue.get()
        # Appending all child nodes so that the explored region of the map can be plotted.
        all_nodes.append([present_node.x, present_node.y])
        # Creating a dict key for identification of node individually
        present_id = key(present_node)
        # The program will exit if the present node is the goal node
        if Check_goal(present_node, goal_node):
            goal_node.parent_id = present_node.parent_id
            goal_node.cost = present_node.cost
            print("Goal Node found")
            end_time = time.time()  # End time for measuring time taken
            time_taken = end_time - start_time  # Calculate time taken
            return all_nodes, 1, time_taken

        if present_id in explored_nodes:
            continue
        else:
            explored_nodes.add(present_id)
        # For all actions in action set, a new child node has to be formed if it is not already explored
        for move in moves:
            x, y, cost = move(present_node.x, present_node.y, present_node.cost)
            # Creating a node class object for all coordinates being explored
            new_node = Node(x, y, cost, present_node)
            new_node_id = key(new_node)

            if not Validity(new_node.x, new_node.y, obs_space):
                continue
            elif new_node_id in explored_nodes:
                continue

            if new_node_id in unexplored_nodes:
                if new_node.cost < unexplored_nodes[new_node_id].cost:
                    unexplored_nodes[new_node_id].cost = new_node.cost
                    unexplored_nodes[new_node_id].parent_id = new_node.parent_id
                    priority_queue.put((new_node.cost, new_node))
            else:
                unexplored_nodes[new_node_id] = new_node
                priority_queue.put((new_node.cost, new_node))

    return all_nodes, 0, 0


# backtrack and generate the shortest path

def Backtrack(goal_node):
    x_path = []
    y_path = []
    x_path.append(goal_node.x)
    y_path.append(goal_node.y)
    # Initialize total cost
    total_cost = goal_node.cost  

    parent_node = goal_node.parent_id
    while parent_node != -1:
        x_path.append(parent_node.x)
        y_path.append(parent_node.y)
        parent_node = parent_node.parent_id

    x_path.reverse()
    y_path.reverse()

    return x_path, y_path, total_cost  # Return total cost along with path coordinates


# Define video properties
output_video_path = "Dijkstra_path_planning_video.mp4"
fps = 60
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_out = cv2.VideoWriter(output_video_path, fourcc, fps, (map_width, map_height))

# Frame counter
frame_counter = 0
frame_interval = 200  # Write every 200th frame

if __name__ == '__main__':
    obs_space = Configuration_space(image)

   #### Taking start node coordinates as input from user #####
    while True:
        start_coordinates = input("Enter coordinates for Start Node (x y): ")
        try:
            s_x, s_y = map(int, start_coordinates.split())
            if not Validity(s_x, s_y, obs_space) or image[s_y][s_x].tolist() == OBS_COLOR or image[s_y][s_x].tolist() == BORDER_COLOR:
                print("Start node is within an obstacle or outside the map boundaries. Please enter valid coordinates.")
                continue
            break
        except ValueError:
            print("Invalid input format. Please enter two integers separated by space.")

    # Taking Goal Node coordinates as input from user
    while True:
        end_coordinates = input("Enter coordinates for Goal Node (x y): ")
        try:
            e_x, e_y = map(int, end_coordinates.split())
            if not Validity(e_x, e_y, obs_space) or image[e_y][e_x].tolist() == OBS_COLOR or image[e_y][e_x].tolist() == BORDER_COLOR:
                print("Goal Node is within an obstacle or outside the map boundaries. Please enter valid coordinates.")
                continue
            print("Processing...")
            break
        except ValueError:
            print("Invalid input format. Please enter two integers separated by space.")

    # Define start and goal nodes
    start_node = Node(s_x, map_height - s_y, 0, -1)  # Start node with cost 0 and no parent
    goal_node = Node(e_x, map_height - e_y, 0, -1)  # You can adjust the goal node coordinates as needed

    # Run Dijkstra algorithm
    all_nodes, found_goal, time_taken = dijkstra(start_node, goal_node, obs_space)

    if found_goal:
        # Generate shortest path
        x_path, y_path, total_cost = Backtrack(goal_node)
        print("Total Cost:", total_cost)
        print("Time taken to find the goal node:", time_taken, "seconds")
    else:
        print("Goal not found.")

    # Visualize the map and path
    image_with_path = np.copy(image)

    if found_goal:
        for idx, node in enumerate(all_nodes):
            cv2.circle(image_with_path, (node[0], node[1]), 1, (0, 255, 255), -1)
            frame_counter += 1

            if frame_counter == frame_interval:
                # Write the frame to video
                video_out.write(image_with_path)
                frame_counter = 0

            # Display the frame
            cv2.imshow("Map with Path", image_with_path)
            cv2.waitKey(1)

        # Draw shortest path
        for i in range(len(x_path) - 1):
            cv2.line(image_with_path, (x_path[i], y_path[i]), (x_path[i + 1], y_path[i + 1]), (0, 255, 0), 2)
            video_out.write(image_with_path)

            # Display the frame
            cv2.imshow("Map with Path", image_with_path)
            cv2.waitKey(1)

        # Draw start and end points
        cv2.circle(image_with_path, (s_x,map_height- s_y), 5, (0, 255, 0), -1)
        cv2.circle(image_with_path, (e_x,map_height- e_y), 5, (0, 0, 255), -1)

        # Write the frame to video
        video_out.write(image_with_path)

        # Display the frame
        cv2.imshow("Map with Path", image_with_path)
        cv2.waitKey(1)

    video_out.release()
    cv2.destroyAllWindows()
