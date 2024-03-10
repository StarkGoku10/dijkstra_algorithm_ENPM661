import numpy as np
import math
import heapq
import cv2

map_width = 1200
map_height = 500

# Create a blank white image
image = np.ones((map_height, map_width, 3), dtype=np.uint8) * 255

# Draw black border around the map
border_thickness = 5
cv2.rectangle(image, (0, 0), (map_width - 1, map_height - 1), (141, 3,6), border_thickness)

polygon_sides = 6
polygon_length = 150
polygon_bloat = 5
PADDING_COLOR= (141,31,6)
OBS_COLOR = (31, 103, 255)
padding = 5

# Draw rectangles with padding
cv2.rectangle(image, (100 - padding,  0- padding), (175 + padding, 400 + padding), PADDING_COLOR, -1)
cv2.rectangle(image, (100 , 0), (175 , 400 ), OBS_COLOR, -1)
cv2.rectangle(image, (275 - padding, 100 - padding), (350 + padding, 500 + padding), PADDING_COLOR, -1)
cv2.rectangle(image, (275 , 100), (350, 500), OBS_COLOR, -1)
# Calculate the vertices of the polygon with padding
polygon_vertices = []
for i in range(polygon_sides):
    angle = np.radians(i * (360 / polygon_sides) + 90)
    x = 650 + ((polygon_length ) * np.cos(angle))
    y = 250 + ((polygon_length ) * np.sin(angle))
    polygon_vertices.append((int(x), int(y)))

# Draw the polygon
cv2.fillPoly(image, [np.array(polygon_vertices)], OBS_COLOR)
cv2.polylines(image, [np.array(polygon_vertices)], isClosed=True, color=(141,31,6), thickness=5)

# Draw U-shaped rectangle with padding
cv2.rectangle(image, (1020 - padding, 50 - padding), (1100 + padding, 450 + padding), PADDING_COLOR, -1)  # Right vertical part of U
cv2.rectangle(image, (1020 , 50), (1100 , 450 ), OBS_COLOR, -1)
cv2.rectangle(image, (900 - padding, 50 - padding), (1100 + padding, 125 + padding), PADDING_COLOR, -1)  # Top vertical part of U
cv2.rectangle(image, (900 , 50), (1100 , 125 ), OBS_COLOR, -1)
cv2.rectangle(image, (900 - padding, 375 - padding), (1100 + padding, 450 + padding), PADDING_COLOR, -1)  # Bottom Horizontal part of U
cv2.rectangle(image, (900 , 375), (1100 , 450 ), OBS_COLOR, -1)

map_width = 1200
map_height = 500

########## DEFINING A NODE CLASS TO STORE NODES AS OBJECTS ###############

class Node:
    def __init__(self, x, y, cost, parent_id):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent_id = parent_id
    
    def __lt__(self, other):
        return self.cost < other.cost

############ CONFIGURATION SPACE CONSTRUCTION WITH OBSTACLES ############

def Configuration_space(image):
    obs_space = np.zeros((map_height, map_width), dtype=np.uint8)
    for y in range(map_height):
        for x in range(map_width):
            if np.all(image[y, x] == PADDING_COLOR):
                obs_space[y, x] = 255
    return obs_space

############## CHECK IF THE GIVEN MOVE IS VALID OR NOT ###############

def Validity(x, y, obs_space):
    # Check if coordinates are within the boundaries of the obstacle space and if the cell is occupied by an obstacle (value 255)
    if x < 0 or x >= map_width or y < 0 or y >= map_height or obs_space[y][x] == 255:
        return False
    return True

############## CHECK IF THE GOAL NODE IS REACHED ###############

def Check_goal(present, goal):
    return present.x == goal.x and present.y == goal.y

############# GENERATE UNIQUE KEY ##############

def key(node):
    return 1022 * node.x + 111 * node.y 

############# GENERATE CHILD NODES ##############

def up(x, y, cost):
    return x, y - 1, cost + 1

def down(x, y, cost):
    return x, y + 1, cost + 1

def left(x, y, cost):
    return x - 1, y, cost + 1

def right(x, y, cost):
    return x + 1, y, cost + 1

def bottom_left(x, y, cost):
    return x - 1, y + 1, cost + 1.414

def bottom_right(x, y, cost):
    return x + 1, y + 1, cost + 1.414

def up_left(x, y, cost):
    return x - 1, y - 1, cost + 1.414

def up_right(x, y, cost):
    return x + 1, y - 1, cost + 1.414

######### IMPLEMENTING DIJKSTRA ALGORITHM ##############

def dijkstra(start, goal, obs_space):
    if not Validity(start.x, start.y, obs_space):
        print("Invalid start node")
        return None, 0
    
    if not Validity(goal.x, goal.y, obs_space):
        print("Invalid goal node")
        return None, 0

    if Check_goal(start, goal):
        return None, 1

    goal_node = goal
    start_node = start
    
    moves = [up, down, left, right, bottom_left, bottom_right, up_left, up_right]
    unexplored_nodes = {}  # List of all open nodes
    
    start_key = key(start_node)  # Generating a unique key for identifying the node
    unexplored_nodes[start_key] = start_node
    
    explored_nodes = {}  # List of all closed nodes
    priority_list = []  # List to store all dictionary entries with cost as the sorting variable
    heapq.heappush(priority_list, [start_node.cost, start_node])  # This Data structure will prioritize the node to be explored which has less cost.
    
    all_nodes = []  # stores all nodes that have been traversed, for visualization purposes.

    while len(priority_list) != 0:
        # Popping the first element in the priority list to create child nodes for exploration
        present_node = (heapq.heappop(priority_list))[1]
        # Appending all child nodes so that the explored region of the map can be plotted.
        all_nodes.append([present_node.x, present_node.y])
        # Creating a dict key for identification of node individually
        present_id = key(present_node)
        # The program will exist if the present node is the goal node
        if Check_goal(present_node, goal_node):
            goal_node.parent_id = present_node.parent_id
            goal_node.cost = present_node.cost
            print("Goal Node found")
            return all_nodes, 1

        if present_id in explored_nodes:  
            continue
        else:
            explored_nodes[present_id] = present_node
        # Deleting the node from the open nodes list because it has been explored and further its child nodes will be generated   
        del unexplored_nodes[present_id]
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
            else:
                unexplored_nodes[new_node_id] = new_node
            
            heapq.heappush(priority_list, [new_node.cost, new_node])
   
    return all_nodes, 0

########### BACKTRACK AND GENERATE SHORTEST PATH ############

def Backtrack(goal_node):  
    x_path = []
    y_path = []
    x_path.append(goal_node.x)
    y_path.append(goal_node.y)

    parent_node = goal_node.parent_id
    while parent_node != -1:
        x_path.append(parent_node.x)
        y_path.append(parent_node.y)
        parent_node = parent_node.parent_id
        
    x_path.reverse()
    y_path.reverse()
    
    return x_path, y_path

######### CALLING ALL MY FUNCTIONS TO IMPLEMENT DIJKSTRA ALGORITHM ON A POINT ROBOT ###########

if __name__ == '__main__':
    obs_space = Configuration_space(image)
    
    #### Taking start node coordinates as input from user #####
    start_coordinates = input("Enter coordinates for Start Node: ")
    s_x, s_y = map(int, start_coordinates.split())
    end_coordinates = input("Enter coordinates for End Node: ")
    e_x, e_y = map(int, end_coordinates.split())

    # Define start and goal nodes
    start_node = Node(s_x, s_y, 0, -1)  # Start node with cost 0 and no parent
    goal_node = Node(e_x, e_y, 0, -1)  # You can adjust the goal node coordinates as needed

    # Run Dijkstra algorithm
    all_nodes, found_goal = dijkstra(start_node, goal_node, obs_space)

    if found_goal:
        # Generate shortest path
        x_path, y_path = Backtrack(goal_node)
        print("Shortest Path: ", x_path, y_path)
    else:
        print("Goal not found or start/goal nodes are invalid.")

    # Visualize the map and path
    image_with_path = np.copy(image)
    
    if found_goal:
        # Draw explored nodes
        for node in all_nodes:
            cv2.circle(image_with_path, (node[0], node[1]), 1, (0, 255, 255), -1)  # Yellow circle for explored nodes

        # Draw shortest path
        for i in range(len(x_path) - 1):
            cv2.line(image_with_path, (x_path[i], y_path[i]), (x_path[i + 1], y_path[i + 1]), (255, 0, 0), 2)

        # Draw start and end points
        cv2.circle(image_with_path, (s_x, s_y), 5, (0, 255, 0), -1)  # Green circle for start point
        cv2.circle(image_with_path, (e_x, e_y), 5, (0, 0, 255), -1)  # Red circle for end point

        cv2.imshow("Map with Path", image_with_path)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
