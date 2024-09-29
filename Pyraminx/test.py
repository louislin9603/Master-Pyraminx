from tkinter import *
from tkinter import ttk
import random
import heapq
from heapq import heapify, heappush
import copy
import time

# Initial state of the Pyraminx in a solved configuration
# 0 = Red, 1 = Blue, 2 = Green, 3 = Yellow 
startingcolors = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

# Make a copy of the starting colors as a goal state
startingcopy = startingcolors


# Node class to keep information about each configuration in A* solve algorithm
class Node():
    def __init__(self, parent = None, configuration = None):
        self.parent = parent
        self.configuration = configuration   # Configuration of pyraminx
        self.g = 0                           # Distance from start to current node
        self.h = 0                           # Heuristic cost to goal
        self.f = 0                           # Total cost (f = g + h)

    # Allows node to be compared based on f-value
    def __lt__(self, other):
        return self.f < other.f

# Heuristic function: Max number of unique colors on any face - 1
def findHeuristic(currentPyramid):

    # Create a list to hold the colors for each of the faces
    color_faces = [[] for _ in range(4)]  
    
    # Map color IDs to their respective faces
    for index, color_id in enumerate(currentPyramid):
        if index < 16:  
            color_faces[0].append(color_id)  # First face (0-15)
        elif index < 32:
            color_faces[1].append(color_id)  # Second face (16-31)
        elif index < 48:
            color_faces[2].append(color_id)  # Third face (32-47)
        else:
            color_faces[3].append(color_id)  # Fourth face (48-63)
    
    max_colors = 0
    
    # Iterate through and count distinct colors on each face
    for face in color_faces:
        distinct_colors = len(set(face))  # Set gets rid of duplicates
        if distinct_colors > max_colors:
            max_colors = distinct_colors

    # Heuristic: max number of distinct colors minus one
    return max_colors - 1

# A* search algorithm to solve the puzzle: 
def solve(initial_state, goal_state):

    start_time = time.time()

    # Initialize start node and get the initial configuration
    startNode = Node(None, initial_state)
    startNode.configuration = initial_state
    startNode.g = 0
    startNode.h = findHeuristic(initial_state)
    startNode.f = startNode.g + startNode.h
    print(f"Initial heuristic: ", startNode.f)
    
    # Initialize end goal 
    endNode = Node(None, goal_state)
    endNode.g = endNode.h = endNode.f = 0   # No cost, since it's the goal

    open_list = []      # Priority queue (min-heap) to store unvisited nodes
    closed_list = []     # List to store visited nodes

    # Add start node to the heap (open list) and change it to a heap
    heappush(open_list, startNode)
    heapify(open_list)

    incrementer = 0     # Count nodes searched

    while (open_list):

        # Select current node (lowest f-value)
        current_node = open_list[0]

        if current_node.configuration is None:
            print("Error: current_node.configuration at top is missing (None)!")

        # Pop the current node 
        heapq.heappop(open_list)             
        closed_list.append(current_node)       # Add the node to closed list

        incrementer += 1

        # Check to see if current node is our solved state
        if solved(current_node.configuration, goal_state):

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Calculate hours, minutes, and seconds
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Display elapsed time in hours, minutes, and seconds
            print(f"Time elapsed: {int(hours)} hours, {int(minutes)} minutes, {seconds:.2f} seconds")
            print("Nodes searched: ", incrementer)
            global current_colors
            current_colors = current_node.configuration
            updateGui()     # Update GUI after configuration is solved

            # Print optimal path from start to goal through parent node
            path = []
            current = current_node
            while current is not None:

                path.append(current.configuration)      # Add configuration to path
                current = current.parent
            for i, config in enumerate(reversed(path)): # Prints each map
                print(f"Step {i + 1}: {config}")
            break

        possible_moves = get_possible_moves()
        
        # Generates a child node for each possible move w/o changing the main
        for move in possible_moves:

            # Create a new instance clone 
            current_nodeClone = copy.deepcopy(current_node)
            # Simulate the moves on the clone
            current_nodeClone.configuration = apply_moves(current_nodeClone.configuration, move)
            
            # Create a new children node from current node for the updated configuration
            child = Node(parent = current_node, configuration = current_nodeClone.configuration)
            child.g = current_node.g + 1
            child.h = findHeuristic(child.configuration)
            child.f = child.g + child.h

            #If a child has been visited, skip it
            if any(node.configuration == child.configuration for node in closed_list):
                continue
                
            # Push new child onto open_list to explore later
            heapq.heappush(open_list,child)

        # Reorganize heap after all children added
        heapify(open_list)   

# Applies move on a configuration for A*
def apply_moves(configuration, move):
    new_configuration = move(configuration)
    return new_configuration

# Returns all rotations for A*
def get_possible_moves():
    possible_moves = []

    possible_moves.append(rotate1)
    possible_moves.append(rotate2)
    possible_moves.append(rotate3)
    possible_moves.append(rotate4)
    possible_moves.append(rotate5)
    possible_moves.append(rotate6)
    possible_moves.append(rotate7)
    possible_moves.append(rotate8)
    possible_moves.append(rotate9)
    possible_moves.append(rotate10)
    possible_moves.append(rotate11)
    possible_moves.append(rotate12)
    possible_moves.append(rotate13)
    possible_moves.append(rotate14)
    possible_moves.append(rotate15)
    possible_moves.append(rotate16)
    possible_moves.append(rotate17)
    possible_moves.append(rotate18)
    possible_moves.append(rotate19)
    possible_moves.append(rotate20)
    possible_moves.append(rotate21)
    possible_moves.append(rotate22)
    possible_moves.append(rotate23)
    possible_moves.append(rotate24)

    return possible_moves

# Initializes the puzzle in its solved state and contains all the buttons
def reset():
    global startingcolors
    global current_colors
    startingcolors = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
    current_colors = startingcolors

    button_list = [
        {"button": Button(root, text="Red Top Clockwise", bg=colors[0]), "function": make_move, "arrotate13": 0},
        {"button": Button(root, text="Red Top Counterclockwise", bg=colors[0]), "function": make_move, "arrotate13": 1},
        {"button": Button(root, text="Red Second Row Clockwise", bg=colors[0]), "function": make_move, "arrotate13": 2},
        {"button": Button(root, text="Red Second Row Counterclockwise", bg=colors[0]), "function": make_move, "arrotate13": 3},
        {"button": Button(root, text="Red Bottom Row Clockwise", bg=colors[0]), "function": make_move, "arrotate13": 4},
        {"button": Button(root, text="Red Bottom Row Counterclockwise", bg=colors[0]), "function": make_move, "arrotate13": 5},
        {"button": Button(root, text="Blue Top Clockwise", bg=colors[1]), "function": make_move, "arrotate13": 6},
        {"button": Button(root, text="Blue Top Counterclockwise", bg=colors[1]), "function": make_move, "arrotate13": 7},
        {"button": Button(root, text="Blue Second Row Clockwise", bg=colors[1]), "function": make_move, "arrotate13": 8},
        {"button": Button(root, text="Blue Second Row Counterclockwise", bg=colors[1]), "function": make_move, "arrotate13": 9},
        {"button": Button(root, text="Blue Bottom Row Clockwise", bg=colors[1]), "function": make_move, "arrotate13": 10},
        {"button": Button(root, text="Blue Bottom Row Counterclockwise", bg=colors[1]), "function": make_move, "arrotate13": 11},
        {"button": Button(root, text="Green Top Clockwise", bg=colors[2]), "function": make_move, "arrotate13": 12},
        {"button": Button(root, text="Green Top Counterclockwise", bg=colors[2]), "function": make_move, "arrotate13": 13},
        {"button": Button(root, text="Green Second Row Clockwise", bg=colors[2]), "function": make_move, "arrotate13": 14},
        {"button": Button(root, text="Green Second Row Counterclockwise", bg=colors[2]), "function": make_move, "arrotate13": 15},
        {"button": Button(root, text="Green Bottom Row Clockwise", bg=colors[2]), "function": make_move, "arrotate13": 16},
        {"button": Button(root, text="Green Bottom Row Counterclockwise", bg=colors[2]), "function": make_move, "arrotate13": 17},
        {"button": Button(root, text="Yellow Top Clockwise", bg=colors[3]), "function": make_move, "arrotate13": 18},
        {"button": Button(root, text="Yellow Top Counterclockwise", bg=colors[3]), "function": make_move, "arrotate13": 19},
        {"button": Button(root, text="Yellow Second Row Clockwise", bg=colors[3]), "function": make_move, "arrotate13": 20},
        {"button": Button(root, text="Yellow Second Row Counterclockwise", bg=colors[3]), "function": make_move, "arrotate13": 21},
        {"button": Button(root, text="Yellow Bottom Row Clockwise", bg=colors[3]), "function": make_move, "arrotate13": 22},
        {"button": Button(root, text="Yellow Bottom Row Counterclockwise", bg=colors[3]), "function": make_move, "arrotate13": 23},
    ]

    # Formatting the buttons
    x_start = 700  
    y_start = 50  
    row_spacing = 30     # Vertical distance between buttons
    col_spacing = 250    # Horizontal distance between color columns

    # Counters for placing buttons
    current_color = 0
    yval = y_start
    xval = x_start

    # Places the buttons in four columns for each color
    for button_info in button_list:

        button_info["button"].place(x=xval, y=yval)
        button_info["button"].config(command=lambda b=button_info: (
            update_current_button(b),
            b["function"](b["arrotate13"],)
        ))
        
        # Move down the column for the next button
        yval += row_spacing

        # When we reach the end of a color's button set, move to the next column
        if (current_color + 1) % 6 == 0:
            xval += col_spacing
            yval = y_start

        current_color += 1

    updateGui()

# Function to execute a rotate based on button click
def make_move(move):
    # List of rotation functions corresponding to the move indices
    rotation_functions = [
        rotate1, rotate2, rotate3, rotate4, rotate5,
        rotate6, rotate7, rotate8, rotate9, rotate10,
        rotate11, rotate12, rotate13, rotate14, rotate15,
        rotate16, rotate17, rotate18, rotate19, rotate20,
        rotate21, rotate22, rotate23, rotate24
    ]

    # Check if the move index is valid
    if 0 <= move < len(rotation_functions):

        # Call the corresponding rotation function
        rotation_functions[move](current_colors)
    else:
        print("ERROR: Invalid move index")

    updateGui()

# Gets # user input and runs randomize function # of times
def randomizer_func():
    entry_text = entry.get()
    if entry_text.isdigit():
        randomize(int(entry_text))

# Randomizes Pyraminx using rotate functions
def randomize(moves):
    if moves == 0:
        reset()

    rotation_functions = [
        rotate1, rotate2, rotate3, rotate4, rotate5,
        rotate6, rotate7, rotate8, rotate9, rotate10,
        rotate11, rotate12, rotate13, rotate14, rotate15,
        rotate16, rotate17, rotate18, rotate19, rotate20,
        rotate21, rotate22, rotate23, rotate24
    ]

    # Randomly selects a number corresponding to the rotation functions (0-23)
    for _ in range(moves):
        move = random.randint(0, 23)  
        rotation_functions[move](current_colors)  # Call the corresponding rotation function

    updateGui() 
        

# Used for drawing the triangles on GUI
def triangle(x,y):
    x1 = x
    x2 = x - 30
    x3 = x + 30
    y1 =  y - 50
    y2 =  y
    y3 = y2
    return [x1,y1, x2,y2, x3,y3]

def triangle_upsidedown(x,y):
    x1 = x
    x2 = x - 30
    x3 = x + 30
    y1 =  y
    y2 =  y - 50
    y3 = y2
    return [x1,y1, x2,y2, x3,y3]

# Globally stores the current button's information
def update_current_button(button_info):
    global current_button_info
    current_button_info = button_info   # Updates new button info

# Check if current node configuration is solved, used for A*
def solved(a, b):
    if a is None or b is None:
        print("One of the configurations is None!")
        return False
    
    # Loops through all 64 pieces of Pyraminx
    for i in range(64): 
        if a[i] != b[i]:    # a is current_state, b is goal_state 
            return False    # If any piece doesn't match
    return True

# Function to draw the triangles on canvas
def draw_triangles(color_index, x_offset, y_offset):

    # 1st row
    canvas.create_polygon(triangle(x_offset, y_offset), fill=colors[current_colors[color_index]], outline="black")
    
    # 2nd row
    canvas.create_polygon(triangle(x_offset - 40, y_offset + 60), fill=colors[current_colors[color_index + 1]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset, y_offset + 60), fill=colors[current_colors[color_index + 2]], outline="black")
    canvas.create_polygon(triangle(x_offset + 40, y_offset + 60), fill=colors[current_colors[color_index + 3]], outline="black")
    
    # 3rd row
    canvas.create_polygon(triangle(x_offset - 80, y_offset + 120), fill=colors[current_colors[color_index + 4]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset - 40, y_offset + 120), fill=colors[current_colors[color_index + 5]], outline="black")
    canvas.create_polygon(triangle(x_offset, y_offset + 120), fill=colors[current_colors[color_index + 6]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset + 40, y_offset + 120), fill=colors[current_colors[color_index + 7]], outline="black")
    canvas.create_polygon(triangle(x_offset + 80, y_offset + 120), fill=colors[current_colors[color_index + 8]], outline="black")
    
    # 4th row
    canvas.create_polygon(triangle(x_offset - 120, y_offset + 180), fill=colors[current_colors[color_index + 9]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset - 80, y_offset + 180), fill=colors[current_colors[color_index + 10]], outline="black")
    canvas.create_polygon(triangle(x_offset - 40, y_offset + 180), fill=colors[current_colors[color_index + 11]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset, y_offset + 180), fill=colors[current_colors[color_index + 12]], outline="black")
    canvas.create_polygon(triangle(x_offset + 40, y_offset + 180), fill=colors[current_colors[color_index + 13]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset + 80, y_offset + 180), fill=colors[current_colors[color_index + 14]], outline="black")
    canvas.create_polygon(triangle(x_offset + 120, y_offset + 180), fill=colors[current_colors[color_index + 15]], outline="black")

# Updates GUI based on current state
def updateGui():

    canvas.delete("all")    # Clears canvas
    
    # Solved text
    solvedText = canvas.create_text(300, 50, text="Solved!", fill="black", font=('Helvetica 15 bold'))
    if solved(startingcopy, current_colors):
        solvedText = canvas.create_text(300, 50, text="Solved!", fill="black", font=('Helvetica 15 bold'))
    else:
        canvas.itemconfig(solvedText, text= "")

    # Draw triangles for each color layer
    draw_triangles(0, 800, 400)     # Red
    draw_triangles(16, 450, 400)    # Blue
    draw_triangles(32, 800, 650)    # Yellow
    draw_triangles(48, 1150, 400)   # Green

#------------------------- ROTATIONS -------------------------------------#
'''
For each color (in respective order):
Top Clockwise
Top Counterclockwise
Second Row Clockwise
Second Row Counterclockwise
Bottom Row Clockwise
Bottom Row Counterclockwise
''' 
# RED
def rotate1(pcolors):
    temp = pcolors[16]
    pcolors[16] = pcolors[63]
    pcolors[63] = pcolors[41]
    pcolors[41] = temp

    updateGui()
    return pcolors
def rotate2(pcolors):
    temp = pcolors[41]
    pcolors[41] = pcolors[63]
    pcolors[63] = pcolors[16]
    pcolors[16] = temp

    updateGui()
    return pcolors
def rotate3(pcolors):
    temp = pcolors[36]
    pcolors[36] = pcolors[19]
    pcolors[19] = pcolors[61]
    pcolors[61] = temp

    temp = pcolors[42]
    pcolors[42] = pcolors[18]
    pcolors[18] = pcolors[62]
    pcolors[62] = temp

    temp = pcolors[43]
    pcolors[43] = pcolors[17]
    pcolors[17] = pcolors[56]
    pcolors[56] = temp
    updateGui()
    return pcolors
def rotate4(pcolors):
    temp = pcolors[61]
    pcolors[61] = pcolors[19]
    pcolors[19] = pcolors[36]
    pcolors[36] = temp

    temp = pcolors[62]
    pcolors[62] = pcolors[18]
    pcolors[18] = pcolors[42]
    pcolors[42] = temp

    temp = pcolors[56]
    pcolors[56] = pcolors[17]
    pcolors[17] = pcolors[43]
    pcolors[43] = temp
    updateGui()
    return pcolors
def rotate5(pcolors):
    temp = pcolors[32]
    pcolors[32] = pcolors[31]
    pcolors[31] = pcolors[57]
    pcolors[57] = temp

    temp = pcolors[34]
    pcolors[34] = pcolors[30]
    pcolors[30] = pcolors[58]
    pcolors[58] = temp

    temp = pcolors[35]
    pcolors[35] = pcolors[29]
    pcolors[29] = pcolors[52]
    pcolors[52] = temp

    temp = pcolors[39]
    pcolors[39] = pcolors[28]
    pcolors[28] = pcolors[53]
    pcolors[53] = temp

    temp = pcolors[40]
    pcolors[40] = pcolors[27]
    pcolors[27] = pcolors[49]
    pcolors[49] = temp

    temp = pcolors[46]
    pcolors[46] = pcolors[26]
    pcolors[26] = pcolors[50]
    pcolors[50] = temp

    temp = pcolors[47]
    pcolors[47] = pcolors[25]
    pcolors[25] = pcolors[48]
    pcolors[48] = temp

    temp = pcolors[0]
    pcolors[0] = pcolors[9]
    pcolors[9] = pcolors[15]
    pcolors[15] = temp

    temp = pcolors[1]
    pcolors[1] = pcolors[11]
    pcolors[11] = pcolors[8]
    pcolors[8] = temp

    temp = pcolors[4]
    pcolors[4] = pcolors[13]
    pcolors[13] = pcolors[3]
    pcolors[3] = temp

    temp = pcolors[2]
    pcolors[2] = pcolors[10]
    pcolors[10] = pcolors[14]
    pcolors[14] = temp

    temp = pcolors[5]
    pcolors[5] = pcolors[12]
    pcolors[12] = pcolors[7]
    pcolors[7] = temp
    updateGui()
    return pcolors
def rotate6(pcolors):
    temp = pcolors[57]
    pcolors[57] = pcolors[31]
    pcolors[31] = pcolors[32]
    pcolors[32] = temp

    temp = pcolors[58]
    pcolors[58] = pcolors[30]
    pcolors[30] = pcolors[34]
    pcolors[34] = temp

    temp = pcolors[52]
    pcolors[52] = pcolors[29]
    pcolors[29] = pcolors[35]
    pcolors[35] = temp

    temp = pcolors[53]
    pcolors[53] = pcolors[28]
    pcolors[28] = pcolors[39]
    pcolors[39] = temp

    temp = pcolors[49]
    pcolors[49] = pcolors[27]
    pcolors[27] = pcolors[40]
    pcolors[40] = temp

    temp = pcolors[50]
    pcolors[50] = pcolors[26]
    pcolors[26] = pcolors[46]
    pcolors[46] = temp

    temp = pcolors[48]
    pcolors[48] = pcolors[25]
    pcolors[25] = pcolors[47]
    pcolors[47] = temp

    temp = pcolors[15]
    pcolors[15] = pcolors[9]
    pcolors[9] = pcolors[0]
    pcolors[0] = temp

    temp = pcolors[8]
    pcolors[8] = pcolors[11]
    pcolors[11] = pcolors[1]
    pcolors[1] = temp

    temp = pcolors[3]
    pcolors[3] = pcolors[13]
    pcolors[13] = pcolors[4]
    pcolors[4] = temp

    temp = pcolors[14]
    pcolors[14] = pcolors[10]
    pcolors[10] = pcolors[2]
    pcolors[2] = temp

    temp = pcolors[7]
    pcolors[7] = pcolors[12]
    pcolors[12] = pcolors[5]
    pcolors[5] = temp
    updateGui()
    return pcolors
# BLUE
def rotate7(pcolors):
    temp = pcolors[47]
    pcolors[47] = pcolors[0]
    pcolors[0] = pcolors[57]
    pcolors[57] = temp
    updateGui()
    return pcolors
def rotate8(pcolors):
    temp = pcolors[57]
    pcolors[57] = pcolors[0]
    pcolors[0] = pcolors[47]
    pcolors[47] = temp
    updateGui()
    return pcolors
def rotate9(pcolors):
    temp = pcolors[45]
    pcolors[45] = pcolors[1]
    pcolors[1] = pcolors[52]
    pcolors[52] = temp

    temp = pcolors[46]
    pcolors[46] = pcolors[2]
    pcolors[2] = pcolors[58]
    pcolors[58] = temp

    temp = pcolors[40]
    pcolors[40] = pcolors[3]
    pcolors[3] = pcolors[59]
    pcolors[59] = temp
    updateGui()
    return pcolors
def rotate10(pcolors):
    temp = pcolors[52]
    pcolors[52] = pcolors[1]
    pcolors[1] = pcolors[45]
    pcolors[45] = temp

    temp = pcolors[58]
    pcolors[58] = pcolors[2]
    pcolors[2] = pcolors[46]
    pcolors[46] = temp

    temp = pcolors[59]
    pcolors[59] = pcolors[3]
    pcolors[3] = pcolors[40]
    pcolors[40] = temp
    updateGui()
    return pcolors
def rotate11(pcolors):
    temp = pcolors[41]
    pcolors[41] = pcolors[9]
    pcolors[9] = pcolors[48]
    pcolors[48] = temp

    temp = pcolors[42]
    pcolors[42] = pcolors[10]
    pcolors[10] = pcolors[50]
    pcolors[50] = temp

    temp = pcolors[36]
    pcolors[36] = pcolors[11]
    pcolors[11] = pcolors[51]
    pcolors[51] = temp

    temp = pcolors[37]
    pcolors[37] = pcolors[12]
    pcolors[12] = pcolors[55]
    pcolors[55] = temp

    temp = pcolors[33]
    pcolors[33] = pcolors[13]
    pcolors[13] = pcolors[56]
    pcolors[56] = temp

    temp = pcolors[34]
    pcolors[34] = pcolors[14]
    pcolors[14] = pcolors[62]
    pcolors[62] = temp

    temp = pcolors[32]
    pcolors[32] = pcolors[15]
    pcolors[15] = pcolors[63]
    pcolors[63] = temp

    temp = pcolors[31]
    pcolors[31] = pcolors[25]
    pcolors[25] = pcolors[16]
    pcolors[16] = temp

    temp = pcolors[24]
    pcolors[24] = pcolors[27]
    pcolors[27] = pcolors[17]
    pcolors[17] = temp

    temp = pcolors[19]
    pcolors[19] = pcolors[29]
    pcolors[29] = pcolors[20]
    pcolors[20] = temp

    temp = pcolors[30]
    pcolors[30] = pcolors[26]
    pcolors[26] = pcolors[18]
    pcolors[18] = temp

    temp = pcolors[23]
    pcolors[23] = pcolors[28]
    pcolors[28] = pcolors[21]
    pcolors[21] = temp
    updateGui()
    return pcolors
def rotate12(pcolors):
    temp = pcolors[48]
    pcolors[48] = pcolors[9]
    pcolors[9] = pcolors[41]
    pcolors[41] = temp

    temp = pcolors[50]
    pcolors[50] = pcolors[10]
    pcolors[10] = pcolors[42]
    pcolors[42] = temp

    temp = pcolors[51]
    pcolors[51] = pcolors[11]
    pcolors[11] = pcolors[36]
    pcolors[36] = temp

    temp = pcolors[55]
    pcolors[55] = pcolors[12]
    pcolors[12] = pcolors[37]
    pcolors[37] = temp

    temp = pcolors[56]
    pcolors[56] = pcolors[13]
    pcolors[13] = pcolors[33]
    pcolors[33] = temp

    temp = pcolors[62]
    pcolors[62] = pcolors[14]
    pcolors[14] = pcolors[34]
    pcolors[34] = temp

    temp = pcolors[63]
    pcolors[63] = pcolors[15]
    pcolors[15] = pcolors[32]
    pcolors[32] = temp

    temp = pcolors[16]
    pcolors[16] = pcolors[25]
    pcolors[25] = pcolors[31]
    pcolors[31] = temp

    temp = pcolors[17]
    pcolors[17] = pcolors[27]
    pcolors[27] = pcolors[24]
    pcolors[24] = temp

    temp = pcolors[20]
    pcolors[20] = pcolors[29]
    pcolors[29] = pcolors[19]
    pcolors[19] = temp

    temp = pcolors[18]
    pcolors[18] = pcolors[26]
    pcolors[26] = pcolors[30]
    pcolors[30] = temp

    temp = pcolors[21]
    pcolors[21] = pcolors[28]
    pcolors[28] = pcolors[23]
    pcolors[23] = temp
    updateGui()
    return pcolors
# GREEN
def rotate13(pcolors):
    temp = pcolors[48]
    pcolors[48] = pcolors[15]
    pcolors[15] = pcolors[31]
    pcolors[31] = temp
    updateGui()
    return pcolors
def rotate14(pcolors):
    temp = pcolors[31]
    pcolors[31] = pcolors[15]
    pcolors[15] = pcolors[48]
    pcolors[48] = temp
    updateGui()
    return pcolors
def rotate15(pcolors):
    temp = pcolors[49]
    pcolors[49] = pcolors[13]
    pcolors[13] = pcolors[24]
    pcolors[24] = temp

    temp = pcolors[50]
    pcolors[50] = pcolors[14]
    pcolors[14] = pcolors[30]
    pcolors[30] = temp

    temp = pcolors[51]
    pcolors[51] = pcolors[8]
    pcolors[8] = pcolors[29]
    pcolors[29] = temp
    updateGui()
    return pcolors
def rotate16(pcolors):
    temp = pcolors[24]
    pcolors[24] = pcolors[13]
    pcolors[13] = pcolors[49]
    pcolors[49] = temp

    temp = pcolors[30]
    pcolors[30] = pcolors[14]
    pcolors[14] = pcolors[50]
    pcolors[50] = temp

    temp = pcolors[29]
    pcolors[29] = pcolors[8]
    pcolors[8] = pcolors[51]
    pcolors[51] = temp
    updateGui()
    return pcolors
def rotate17(pcolors):
    temp = pcolors[63]
    pcolors[63] = pcolors[0]
    pcolors[0] = pcolors[25]
    pcolors[25] = temp

    temp = pcolors[62]
    pcolors[62] = pcolors[2]
    pcolors[2] = pcolors[26]
    pcolors[26] = temp

    temp = pcolors[61]
    pcolors[61] = pcolors[1]
    pcolors[1] = pcolors[20]
    pcolors[20] = temp

    temp = pcolors[60]
    pcolors[60] = pcolors[5]
    pcolors[5] = pcolors[21]
    pcolors[21] = temp

    temp = pcolors[59]
    pcolors[59] = pcolors[4]
    pcolors[4] = pcolors[17]
    pcolors[17] = temp

    temp = pcolors[58]
    pcolors[58] = pcolors[10]
    pcolors[10] = pcolors[18]
    pcolors[18] = temp

    temp = pcolors[57]
    pcolors[57] = pcolors[9]
    pcolors[9] = pcolors[16]
    pcolors[16] = temp

    temp = pcolors[47]
    pcolors[47] = pcolors[41]
    pcolors[41] = pcolors[32]
    pcolors[32] = temp

    temp = pcolors[40]
    pcolors[40] = pcolors[43]
    pcolors[43] = pcolors[33]
    pcolors[33] = temp

    temp = pcolors[35]
    pcolors[35] = pcolors[45]
    pcolors[45] = pcolors[36]
    pcolors[36] = temp

    temp = pcolors[46]
    pcolors[46] = pcolors[42]
    pcolors[42] = pcolors[34]
    pcolors[34] = temp

    temp = pcolors[39]
    pcolors[39] = pcolors[44]
    pcolors[44] = pcolors[37]
    pcolors[37] = temp
    updateGui()
    return pcolors
def rotate18(pcolors):
    temp = pcolors[25]
    pcolors[25] = pcolors[0]
    pcolors[0] = pcolors[63]
    pcolors[63] = temp

    temp = pcolors[26]
    pcolors[26] = pcolors[2]
    pcolors[2] = pcolors[62]
    pcolors[62] = temp

    temp = pcolors[20]
    pcolors[20] = pcolors[1]
    pcolors[1] = pcolors[61]
    pcolors[61] = temp

    temp = pcolors[21]
    pcolors[21] = pcolors[5]
    pcolors[5] = pcolors[60]
    pcolors[60] = temp

    temp = pcolors[17]
    pcolors[17] = pcolors[4]
    pcolors[4] = pcolors[59]
    pcolors[59] = temp

    temp = pcolors[18]
    pcolors[18] = pcolors[10]
    pcolors[10] = pcolors[58]
    pcolors[58] = temp

    temp = pcolors[16]
    pcolors[16] = pcolors[9]
    pcolors[9] = pcolors[57]
    pcolors[57] = temp

    temp = pcolors[32]
    pcolors[32] = pcolors[41]
    pcolors[41] = pcolors[47]
    pcolors[47] = temp

    temp = pcolors[33]
    pcolors[33] = pcolors[43]
    pcolors[43] = pcolors[40]
    pcolors[40] = temp

    temp = pcolors[36]
    pcolors[36] = pcolors[45]
    pcolors[45] = pcolors[35]
    pcolors[35] = temp

    temp = pcolors[34]
    pcolors[34] = pcolors[42]
    pcolors[42] = pcolors[46]
    pcolors[46] = temp

    temp = pcolors[37]
    pcolors[37] = pcolors[44]
    pcolors[44] = pcolors[39]
    pcolors[39] = temp
    updateGui()
    return pcolors
# YELLOW
def rotate19(pcolors):
    temp = pcolors[32]
    pcolors[32] = pcolors[25]
    pcolors[25] = pcolors[9]
    pcolors[9] = temp
    updateGui()
    return pcolors
def rotate20(pcolors):
    temp = pcolors[9]
    pcolors[9] = pcolors[25]
    pcolors[25] = pcolors[32]
    pcolors[32] = temp
    updateGui()
    return pcolors
def rotate21(pcolors):
    temp = pcolors[27]
    pcolors[27] = pcolors[4]
    pcolors[4] = pcolors[33]
    pcolors[33] = temp

    temp = pcolors[26]
    pcolors[26] = pcolors[10]
    pcolors[10] = pcolors[34]
    pcolors[34] = temp

    temp = pcolors[20]
    pcolors[20] = pcolors[11]
    pcolors[11] = pcolors[35]
    pcolors[35] = temp
    updateGui()
    return pcolors
def rotate22(pcolors):
    temp = pcolors[33]
    pcolors[33] = pcolors[4]
    pcolors[4] = pcolors[27]
    pcolors[27] = temp

    temp = pcolors[34]
    pcolors[34] = pcolors[10]
    pcolors[10] = pcolors[26]
    pcolors[26] = temp

    temp = pcolors[35]
    pcolors[35] = pcolors[11]
    pcolors[11] = pcolors[20]
    pcolors[20] = temp
    updateGui()
    return pcolors
def rotate23(pcolors):
    temp = pcolors[41]
    pcolors[41] = pcolors[31]
    pcolors[31] = pcolors[0]
    pcolors[0] = temp

    temp = pcolors[42]
    pcolors[42] = pcolors[30]
    pcolors[30] = pcolors[2]
    pcolors[2] = temp

    temp = pcolors[43]
    pcolors[43] = pcolors[24]
    pcolors[24] = pcolors[3]
    pcolors[3] = temp

    temp = pcolors[44]
    pcolors[44] = pcolors[23]
    pcolors[23] = pcolors[7]
    pcolors[7] = temp

    temp = pcolors[45]
    pcolors[45] = pcolors[19]
    pcolors[19] = pcolors[8]
    pcolors[8] = temp

    temp = pcolors[46]
    pcolors[46] = pcolors[18]
    pcolors[18] = pcolors[14]
    pcolors[14] = temp

    temp = pcolors[47]
    pcolors[47] = pcolors[16]
    pcolors[16] = pcolors[15]
    pcolors[15] = temp

    temp = pcolors[63]
    pcolors[63] = pcolors[57]
    pcolors[57] = pcolors[48]
    pcolors[48] = temp

    temp = pcolors[56]
    pcolors[56] = pcolors[59]
    pcolors[59] = pcolors[49]
    pcolors[49] = temp

    temp = pcolors[51]
    pcolors[51] = pcolors[61]
    pcolors[61] = pcolors[52]
    pcolors[52] = temp

    temp = pcolors[62]
    pcolors[62] = pcolors[58]
    pcolors[58] = pcolors[50]
    pcolors[50] = temp

    temp = pcolors[55]
    pcolors[55] = pcolors[60]
    pcolors[60] = pcolors[53]
    pcolors[53] = temp
    updateGui()
    return pcolors
def rotate24(pcolors):
    temp = pcolors[0]
    pcolors[0] = pcolors[31]
    pcolors[31] = pcolors[41]
    pcolors[41] = temp

    temp = pcolors[2]
    pcolors[2] = pcolors[30]
    pcolors[30] = pcolors[42]
    pcolors[42] = temp

    temp = pcolors[3]
    pcolors[3] = pcolors[24]
    pcolors[24] = pcolors[43]
    pcolors[43] = temp

    temp = pcolors[7]
    pcolors[7] = pcolors[23]
    pcolors[23] = pcolors[44]
    pcolors[44] = temp

    temp = pcolors[8]
    pcolors[8] = pcolors[19]
    pcolors[19] = pcolors[45]
    pcolors[45] = temp

    temp = pcolors[14]
    pcolors[14] = pcolors[18]
    pcolors[18] = pcolors[46]
    pcolors[46] = temp

    temp = pcolors[15]
    pcolors[15] = pcolors[16]
    pcolors[16] = pcolors[47]
    pcolors[47] = temp

    temp = pcolors[48]
    pcolors[48] = pcolors[57]
    pcolors[57] = pcolors[63]
    pcolors[63] = temp

    temp = pcolors[49]
    pcolors[49] = pcolors[59]
    pcolors[59] = pcolors[56]
    pcolors[56] = temp

    temp = pcolors[52]
    pcolors[52] = pcolors[61]
    pcolors[61] = pcolors[51]
    pcolors[51] = temp

    temp = pcolors[50]
    pcolors[50] = pcolors[58]
    pcolors[58] = pcolors[62]
    pcolors[62] = temp

    temp = pcolors[53]
    pcolors[53] = pcolors[60]
    pcolors[60] = pcolors[55]
    pcolors[55] = temp
    updateGui()
    return pcolors

# --------------------- MAIN -------------------------#
root = Tk()
root.title("Pyraminx")
canvas = Canvas(root, width=3000, height=2000)
colors = ["red", "blue", "yellow", "green", "black"]
canvas.pack()

reset()

# Randomize Button
button = Button(root, text="Randomize", command=randomizer_func, bg = 'grey', font=(150))
button.place(x = 1650, y = 600)

# User Input for randomize
entry = Entry(root, font=(200))
entry.place(x = 1400,  y = 600)

# A* Solve
searchButton = Button(root, text="Solve", command=lambda: solve(current_colors, startingcopy), bg='gray', font=(300))
searchButton.place(x = 1650, y = 650)
root.mainloop()