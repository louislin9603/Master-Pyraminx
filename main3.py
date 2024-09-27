from tkinter import *
from tkinter import ttk
import random
import heapq
from heapq import heapify, heappush
import copy

#For confidentiality reasons that were mentioned by ,my professor
#I the author was warned not to put my name in this code.
#Therefore, I will refer to myself as the author and the friend who wrote the basics of the GUI as the Peer.
#From hereon, Peer code will be designated as such, and otherwise the code will be mine as the Author.

flag = 0    #GUI toggle
counterClockToggle = 0  #A* search toggle
startingcolors = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
startingcopy = startingcolors


#Holds node data for A*
class Node():
    def __init__(self, parent = None, configuration = None):
        self.parent = parent
        self.configuration = configuration #Configuration of pyraminx
        self.g = 0  #Distance from start to current node
        self.h = 0  #Heuristic cost to goal
        self.f = 0  #Total cost (g + h)

    #Allow heap to compare nodes based on f value
    def __lt__(self, other):
        return self.f < other.f

def findHeuristic(currentPyramid):
    # Assuming currentPyramid is a list of color IDs
    color_faces = [[] for _ in range(4)]  # List to hold colors for each face
    
    # Map color IDs to their respective faces
    for index, color_id in enumerate(currentPyramid):
        if index < 16:  # Adjust this based on how you define your face sections
            color_faces[0].append(color_id)  # First face
        elif index < 32:
            color_faces[1].append(color_id)  # Second face
        elif index < 48:
            color_faces[2].append(color_id)  # Third face
        else:
            color_faces[3].append(color_id)  # Fourth face
    
    max_colors = 0
    
    # Count distinct colors on each face
    for face in color_faces:
        distinct_colors = len(set(face))  # Using set to count unique colors
        if distinct_colors > max_colors:
            max_colors = distinct_colors

    # Heuristic: max number of distinct colors minus one
    return max_colors - 1


#A* search algorithm, called by searchButton
def astar(startPyramid, endPyramid):

    #initialize start and end nodes
    startNode = Node(None, startPyramid)
    startNode.configuration = startPyramid
    startNode.g = startNode.f = 0
    startNode.h = findHeuristic(startPyramid)
    print(startNode.h)
    endNode = Node(None, endPyramid)
    endNode.g = endNode.h = endNode.f = 0

    heap = [] #Store nodes that have not been visited.
    closedList = [] #store visited nodes

    #Create heap queue with start node
    heappush(heap, startNode)
    heapify(heap)

    incrementer = 0
    while (heap):

        #Pick lowest f value
        currentNode = heap[0]
        if currentNode.configuration is None:
            print("Error: currentNode.config at top is None!")

        heapq.heappop(heap)             #Acknowledge we're visiting this node
        closedList.append(currentNode)  #Add node to visited nodes

        incrementer += 1
        #Check to see if current node is our solved pyraminx
        if solved(currentNode.configuration, endPyramid):
            print("Solved!!!")
            print("Nodes searched: ", incrementer)
            global currentcolors
            currentcolors = currentNode.configuration
            updateGui()

            #Print optimal path
            path = []
            current = currentNode
            while current is not None:
                path.append(current.configuration)
                current = current.parent
            for i, config in enumerate(reversed(path)):
                print(f"Step {i + 1}: {config}")
            break

        #Determine what moves can be done to this configuration
        possibleMoves = fetchPossibleMoves()
        
        #Create a child node for each possible move on a configuration
        for move in possibleMoves:
            currentNodeClone = copy.deepcopy(currentNode)
            currentNodeClone.configuration = applyMoves(currentNodeClone.configuration, move)
            child = Node(parent = currentNode, configuration = currentNodeClone.configuration)
            child.g = currentNode.g + 1
            child.h = findHeuristic(child.configuration)
            child.f = child.g + child.h

            #If a child has been visited, don't bother
            if any(node.configuration == child.configuration for node in closedList):
                continue
            heapq.heappush(heap,child)

        heapify(heap)   #Reorganize heap once new children added

#Applies moves on a configuration to produce children (A*)
def applyMoves(configuration, move):
    newConfiguration = move(configuration)
    return newConfiguration

#Returns a list of moves that can be applied to a configuration (A*)
def fetchPossibleMoves():
    possible_moves = []

    possible_moves.append(r1)
    possible_moves.append(r1p)
    possible_moves.append(r2)
    possible_moves.append(r2p)
    possible_moves.append(r3)
    possible_moves.append(r3p)
    possible_moves.append(b1)
    possible_moves.append(b1p)
    possible_moves.append(b2)
    possible_moves.append(b2p)
    possible_moves.append(b3)
    possible_moves.append(b3p)
    possible_moves.append(g1)
    possible_moves.append(g1p)
    possible_moves.append(g2)
    possible_moves.append(g2p)
    possible_moves.append(g3)
    possible_moves.append(g3p)
    possible_moves.append(y1)
    possible_moves.append(y1p)
    possible_moves.append(y2)
    possible_moves.append(y2p)
    possible_moves.append(y3)
    possible_moves.append(y3p)

    return possible_moves


#GUI code is from peer, not from author
def reset():
    global startingcolors
    global currentcolors
    startingcolors = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
    currentcolors = startingcolors

    clock_list = [
        {"button": Button(root, text="top clock", bg = colors[0]), "function": makemove, "arg1": 0},
        {"button": Button(root, text="top counter clock", bg = colors[0]), "function": makemove, "arg1": 1},
        {"button": Button(root, text="second clock", bg = colors[0]), "function": makemove, "arg1": 2},
        {"button": Button(root, text="second counter clock", bg = colors[0]), "function": makemove, "arg1": 3},
        {"button": Button(root, text="bottom clock", bg = colors[0]), "function": makemove, "arg1": 4},
        {"button": Button(root, text="bottom counter clock", bg = colors[0]), "function": makemove, "arg1": 5},
        {"button": Button(root, text="top clock", bg = colors[1]), "function": makemove, "arg1": 6},
        {"button": Button(root, text="top counterclock", bg = colors[1]), "function": makemove, "arg1": 7},
        {"button": Button(root, text="second clock", bg = colors[1]), "function": makemove, "arg1": 8},
        {"button": Button(root, text="second counter clock", bg = colors[1]), "function": makemove, "arg1": 9},
        {"button": Button(root, text="bottom clock", bg = colors[1]), "function": makemove, "arg1": 10},
        {"button": Button(root, text="bottom counter clock", bg = colors[1]), "function": makemove, "arg1": 11},
        {"button": Button(root, text="top clock", bg = colors[2]), "function": makemove, "arg1": 12},
        {"button": Button(root, text="top counter clock", bg = colors[2]), "function": makemove, "arg1": 13},
        {"button": Button(root, text="second clock", bg = colors[2]), "function": makemove, "arg1": 14},
        {"button": Button(root, text="second counter clock", bg = colors[2]), "function": makemove, "arg1": 15},
        {"button": Button(root, text="bottom clock", bg = colors[2]), "function": makemove, "arg1": 16},
        {"button": Button(root, text="bottom counter clock", bg = colors[2]), "function": makemove, "arg1": 17},
        {"button": Button(root, text="top clock", bg = colors[3]), "function": makemove, "arg1": 18},
        {"button": Button(root, text="top counter clock", bg = colors[3]), "function": makemove, "arg1": 19},
        {"button": Button(root, text="second clock", bg = colors[3]), "function": makemove, "arg1": 20},
        {"button": Button(root, text="second counter clock", bg = colors[3]), "function": makemove, "arg1": 21},
        {"button": Button(root, text="bottom clock", bg = colors[3]), "function": makemove, "arg1": 22},
        {"button": Button(root, text="bottom counter clock", bg = colors[3]), "function": makemove, "arg1": 23},
    ]

    yval = 50
    for button_info in clock_list:
        button_info["button"].place(x=1100, y=yval)
        button_info["button"].config(command=lambda b=button_info: (
        update_current_button(b),
        b["function"](b["arg1"],)
        ))
        yval = yval + 30

    updateGui()

def makemove(move):
    match move:
        case 0:
            r1(currentcolors)
        case 1:
            r1p(currentcolors)
        case 2:
            r2(currentcolors)
        case 3:
            r2p(currentcolors)
        case 4:
            r3(currentcolors)
        case 5:
            r3p(currentcolors)
        case 6:
            b1(currentcolors)
        case 7:
            b1p(currentcolors)
        case 8:
            b2(currentcolors)
        case 9:
            b2p(currentcolors)
        case 10:
            b3(currentcolors)
        case 11:
            b3p(currentcolors)
        case 12:
            g1(currentcolors)
        case 13:
            g1p(currentcolors)
        case 14:
            g2(currentcolors)
        case 15:
            g2p(currentcolors)
        case 16:
            g3(currentcolors)
        case 17:
            g3p(currentcolors)
        case 18:
            y1(currentcolors)
        case 19:
            y1p(currentcolors)
        case 20:
            y2(currentcolors)
        case 21:
            y2p(currentcolors)
        case 22:
            y3(currentcolors)
        case 23:
            y3p(currentcolors)
        case _:
            print("ERROR")
    updateGui()
#To save processing power, toggle on/off updating of the graphics
def toggle_func():
    global flag
    global toggleButton, toggleText

    #0 and 2 are off, 1 is on. Set to 0 at runtime, 2 o/w
    if ((flag == 0) or (flag == 2)):
        flag = 1
        toggleText = canvas.create_text(206, 750, text="Performance Mode", fill="black", font=('Helvetica 15 bold'))
        toggleButton.config(bg="green")
    else:
        toggleButton.config(bg="gray")
        flag = 2
        updateGui()

#To save processing power, scramble and solve based on (counter or) clockwise moves
def counterClockToggle_func():
    global counterClockToggle

    #0 is all moves, 1 is counterclockwise, 2 is clockwise
    if (counterClockToggle == 0):
        counterClockToggle = 1
        counterClockToggleButton.config(bg="blue", text = "Counter Moves Only")
    elif (counterClockToggle == 1):
        counterClockToggle = 2
        counterClockToggleButton.config(bg="orange", text = "Clockwise Moves Only")
    else:
        counterClockToggle = 0
        counterClockToggleButton.config(bg="gray", text = "All Moves Possible")

#Peer code that takes user input for randomizer
def randomizer_func():
    entry_text = entry.get()
    if entry_text.isdigit():
        randompyraminx(int(entry_text))

#There are 28 different nonredundant moves in this program.
#Written by Author, not Peer
def randompyraminx(moves):
    if moves == 0:
        reset()

    lowerBound = 0
    upperBound = 27

    if (counterClockToggle == 1):
        lowerBound = 14
        upperBound = 27
    elif (counterClockToggle == 2):
        lowerBound = 0
        upperBound = 13

    for i in range(moves):
        move = random.randint(lowerBound, upperBound)
        match move:
            case 0:
                r1(currentcolors)
            case 1:
                r1p(currentcolors)
            case 2:
                r2(currentcolors)
            case 3:
                r2p(currentcolors)
            case 4:
                r3(currentcolors)
            case 5:
                r3p(currentcolors)
            case 6:
                b1(currentcolors)
            case 7:
                b1p(currentcolors)
            case 8:
                b2(currentcolors)
            case 9:
                b2p(currentcolors)
            case 10:
                b3(currentcolors)
            case 11:
                b3p(currentcolors)
            case 12:
                g1(currentcolors)
            case 13:
                g1p(currentcolors)
            case 14:
                g2(currentcolors)
            case 15:
                g2p(currentcolors)
            case 16:
                g3(currentcolors)
            case 17:
                g3p(currentcolors)
            case 18:
                y1(currentcolors)
            case 19:
                y1p(currentcolors)
            case 20:
                y2(currentcolors)
            case 21:
                y2p(currentcolors)
            case 22:
                y3(currentcolors)
            case 23:
                y3p(currentcolors)
            case _:
                print("ERROR")
    updateGui()     
        

#As this function and the next 3 below it are GUI,
#these were wrote by the peer and not the author
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

def update_current_button(button_info):
    global current_button_info
    current_button_info = button_info

#Check if node current configuration is solved. Also works for A*
def solved(a, b):
    if a is None or b is None:
        print("One of the configurations is None!")
        return False
    for i in range(64):
        if a[i] != b[i]:
            return False
    return True

def draw_triangles(color_index, x_offset, y_offset):
    """Draws triangles for a specific color layer."""
    # 1st row
    canvas.create_polygon(triangle(x_offset, y_offset), fill=colors[currentcolors[color_index]], outline="black")
    
    # 2nd row
    canvas.create_polygon(triangle(x_offset - 40, y_offset + 60), fill=colors[currentcolors[color_index + 1]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset, y_offset + 60), fill=colors[currentcolors[color_index + 2]], outline="black")
    canvas.create_polygon(triangle(x_offset + 40, y_offset + 60), fill=colors[currentcolors[color_index + 3]], outline="black")
    
    # 3rd row
    canvas.create_polygon(triangle(x_offset - 80, y_offset + 120), fill=colors[currentcolors[color_index + 4]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset - 40, y_offset + 120), fill=colors[currentcolors[color_index + 5]], outline="black")
    canvas.create_polygon(triangle(x_offset, y_offset + 120), fill=colors[currentcolors[color_index + 6]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset + 40, y_offset + 120), fill=colors[currentcolors[color_index + 7]], outline="black")
    canvas.create_polygon(triangle(x_offset + 80, y_offset + 120), fill=colors[currentcolors[color_index + 8]], outline="black")
    
    # 4th row
    canvas.create_polygon(triangle(x_offset - 120, y_offset + 180), fill=colors[currentcolors[color_index + 9]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset - 80, y_offset + 180), fill=colors[currentcolors[color_index + 10]], outline="black")
    canvas.create_polygon(triangle(x_offset - 40, y_offset + 180), fill=colors[currentcolors[color_index + 11]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset, y_offset + 180), fill=colors[currentcolors[color_index + 12]], outline="black")
    canvas.create_polygon(triangle(x_offset + 40, y_offset + 180), fill=colors[currentcolors[color_index + 13]], outline="black")
    canvas.create_polygon(triangle_upsidedown(x_offset + 80, y_offset + 180), fill=colors[currentcolors[color_index + 14]], outline="black")
    canvas.create_polygon(triangle(x_offset + 120, y_offset + 180), fill=colors[currentcolors[color_index + 15]], outline="black")
    
def updateGui():
    canvas.delete("all")
    
    solvedText = canvas.create_text(300, 50, text="Solved!", fill="black", font=('Helvetica 15 bold'))
    if solved(startingcopy, currentcolors):
        solvedText = canvas.create_text(300, 50, text="Solved!", fill="black", font=('Helvetica 15 bold'))
    else:
        canvas.itemconfig(solvedText, text= "")

    # Draw triangles for each color layer
    draw_triangles(0, 500, 150)   # Red
    draw_triangles(16, 500, 610)  # Blue
    draw_triangles(32, 300, 330)  # Green
    draw_triangles(48, 700, 330)  # Yellow

#red base moves
def r1(pcolors):
    temp = pcolors[16]
    pcolors[16] = pcolors[63]
    pcolors[63] = pcolors[41]
    pcolors[41] = temp

    updateGui()
    return pcolors

def r1p(pcolors):
    temp = pcolors[41]
    pcolors[41] = pcolors[63]
    pcolors[63] = pcolors[16]
    pcolors[16] = temp

    updateGui()
    return pcolors

def r2(pcolors):
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
def r2p(pcolors):
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
def r3(pcolors):
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
def r3p(pcolors):
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
#blue base moves
def b1(pcolors):
    temp = pcolors[47]
    pcolors[47] = pcolors[0]
    pcolors[0] = pcolors[57]
    pcolors[57] = temp
    updateGui()
    return pcolors
def b1p(pcolors):
    temp = pcolors[57]
    pcolors[57] = pcolors[0]
    pcolors[0] = pcolors[47]
    pcolors[47] = temp
    updateGui()
    return pcolors
def b2(pcolors):
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
def b2p(pcolors):
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
def b3(pcolors):
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
def b3p(pcolors):
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
#green base moves
def g1(pcolors):
    temp = pcolors[48]
    pcolors[48] = pcolors[15]
    pcolors[15] = pcolors[31]
    pcolors[31] = temp
    updateGui()
    return pcolors
def g1p(pcolors):
    temp = pcolors[31]
    pcolors[31] = pcolors[15]
    pcolors[15] = pcolors[48]
    pcolors[48] = temp
    updateGui()
    return pcolors
def g2(pcolors):
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
def g2p(pcolors):
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
def g3(pcolors):
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
def g3p(pcolors):
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
#yellow base moves
def y1(pcolors):
    temp = pcolors[32]
    pcolors[32] = pcolors[25]
    pcolors[25] = pcolors[9]
    pcolors[9] = temp
    updateGui()
    return pcolors
def y1p(pcolors):
    temp = pcolors[9]
    pcolors[9] = pcolors[25]
    pcolors[25] = pcolors[32]
    pcolors[32] = temp
    updateGui()
    return pcolors
def y2(pcolors):
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
def y2p(pcolors):
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
def y3(pcolors):
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
def y3p(pcolors):
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

#MAIN (GUI Code wrote by Peer, with tweaks by Author)
root = Tk()
root.title("Pyraminx")
canvas = Canvas(root, width=1500, height=1000)
colors = ["red", "blue", "yellow", "green", "black"]
canvas.pack()

reset()

#Randomize button and user entry
button = Button(root, text="Randomize", command=randomizer_func, bg = 'grey')
button.place(x = 715, y = 765)
entry = Entry(root)
entry.place(x = 580,  y = 770)

#Toggle graphics button
toggleButton = Button(root, text = "Toggle GUI Update", command = toggle_func, bg = 'gray')
toggleButton.place(x = 150, y = 765)

#Toggle if A* scrambler should only scramble using counter or counterclockwise movements
counterClockToggleButton = Button(root, text = "All Moves Possible", command = counterClockToggle_func, bg = 'gray')
counterClockToggleButton.place(x = 400, y = 765)
counterClockToggleText = canvas.create_text(455, 750, text="A* Moveset", fill="black", font=('Helvetica 15 bold'))

#Button to start A* search
searchButton = Button(root, text="Solve Using A*", command=lambda: astar(currentcolors, startingcopy), bg='gray')
searchButton.place(x = 800, y = 765)
root.mainloop()