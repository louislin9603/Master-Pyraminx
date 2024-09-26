from tkinter import *
from tkinter import ttk
from collections import namedtuple
import random
import copy
import heapq

num_moves = 0

class Pyraminx:
    def __init__(self):
        # Initialize faces with default colors
        self.faces = {
            'A': [["red"] * 4 for _ in range(4)],
            'B': [["green"] * 4 for _ in range(4)],
            'C': [["blue"] * 4 for _ in range(4)],
            'D': [["yellow"] * 4 for _ in range(4)],
        }

        self.original_state = self.faces.copy()

    def get_colors(self):
        # Get a flat list of colors from all faces
        return [color for face in self.faces.values() for row in face for color in row]

    def set_colors(self, colors):
        # Set colors back to faces from a flat list of shuffled colors
        index = 0
        for face in self.faces:
            for i in range(4):
                for j in range(4):
                    self.faces[face][i][j] = colors[index]
                    index += 1
        

class PyraminxGui:
    triangle_id = 0
    def __init__(self, root):
        self.root = root
        self.pyraminx = Pyraminx()
        self.triangles = []  # Store triangle information
        root.title("Pyraminx Puzzle")
        self.State = namedtuple('State', ['colors', 'moves', 'cost', 'heuristic'])

        self.canvas = Canvas(root, width=1000, height=1000, bg='white')

        self.canvas.pack()

        self.buttons = []
        yval = 50

        # Create and position the buttons
        self.create_buttons(yval)
        self.updateGui()

    def create_buttons(self, yval):
        # Randomize Button
        self.input_moves = Entry(self.root)
        self.input_moves.place(x=650, y=yval)

        # Reset Button
        self.reset_button = Button(self.root, text="Reset", command=self.reset_puzzle)
        self.reset_button.place(x=800, y=yval)  # Place the reset button at (x=800, y=yval)
        self.buttons.append(self.reset_button)  # Add to the list

        self.button = Button(self.root, text="Randomize", command=self.randomize_puzzle)
        self.button.place(x=700, y=yval)  # Place the button at (x=820, y=yval)
        self.buttons.append(self.button)  # Add to the list

        self.solve_button = Button(self.root, text="Solve", command=self.solve)
        self.solve_button.place(x=900, y=yval)
        self.buttons.append(self.solve_button)

        # Increment yval to place the buttons close together
        yval += 30

        #----------------------- RED FACE at the bottom -------------------------------------#

        #Button 1 - Top Clockwise
        self.rotate_button1 = Button(self.root, text="Red Clockwise", command=self.rotate1)
        self.rotate_button1.place(x=700, y=yval)
        self.buttons.append(self.rotate_button1)
        yval += 30  # Increment yval for the next button

        #Button 2 - Top Counterclockwise
        self.rotate_button2 = Button(self.root, text="Red Counterclockwise", command=self.rotate2)
        self.rotate_button2.place(x=700, y=yval)
        self.buttons.append(self.rotate_button2)
        yval += 30  # Increment yval for each new button

        #Button 3 - 2nd Row Clockwise
        self.rotate_button3 = Button(self.root, text="Red SecondRow Clockwise", command=self.rotate3)
        self.rotate_button3.place(x=700, y=yval)
        self.buttons.append(self.rotate_button3)
        yval +=30

        #Button 4 - 2nd Row Counterclockwise
        self.rotate_button4 = Button(self.root, text="Red SecondRow Counterclockwise", command=self.rotate4)
        self.rotate_button4.place(x=700, y=yval)
        self.buttons.append(self.rotate_button4)
        yval += 30

        #Button 5 - Last Row Clockwise
        self.rotate_button5 = Button(self.root, text="Red Last Row Clockwise", command=self.rotate5)
        self.rotate_button5.place(x=700, y=yval)
        self.buttons.append(self.rotate_button5)
        yval += 30

        #Button 6 - Last Row Counterclockwise
        self.rotate_button6 = Button(self.root, text="Red Last Row Counterclockwise", command=self.rotate6)
        self.rotate_button6.place(x=700, y=yval)
        self.buttons.append(self.rotate_button6)
        yval += 50

         #----------------------- GREEN FACE at the bottom-------------------------------------#

        #Button 7 - Top Row Clockwise
        self.rotate_button7 = Button(self.root, text="Green Top Clockwise", command=self.rotate7)
        self.rotate_button7.place(x=700, y=yval)
        self.buttons.append(self.rotate_button7)
        yval += 30

        #Button 8 - Top Row Counterclockwise
        self.rotate_button8 = Button(self.root, text="Green Top Counterclockwise", command=self.rotate8)
        self.rotate_button8.place(x=700, y=yval)
        self.buttons.append(self.rotate_button8)
        yval += 30

        #Button 9 - Second Row Clockwise
        self.rotate_button9 = Button(self.root, text="Green SecondRow Clockwise", command=self.rotate9)
        self.rotate_button9.place(x=700, y=yval)
        self.buttons.append(self.rotate_button9)
        yval += 30

        #Button 10 - Second Row Counterclockwise
        self.rotate_button10 = Button(self.root, text="Green SecondRow Counterclockwise", command=self.rotate10)
        self.rotate_button10.place(x=700, y=yval)
        self.buttons.append(self.rotate_button10)
        yval += 30

        #Button 11 - Last Row Counterclockwise
        self.rotate_button11 = Button(self.root, text="Green Last Row Clockwise", command=self.rotate11)
        self.rotate_button11.place(x=700, y=yval)
        self.buttons.append(self.rotate_button11)
        yval += 30

        #Button 12 - Last Row Counterclockwise
        self.rotate_button12 = Button(self.root, text="Green Last Row Counterclockwise", command=self.rotate12)
        self.rotate_button12.place(x=700, y=yval)
        self.buttons.append(self.rotate_button12)
        yval += 50

        #----------------------- YELLOW FACE at the bottom-------------------------------------#

        #Button 13 - Top Row Clockwise
        self.rotate_button13 = Button(self.root, text="Yellow Top Clockwise", command=self.rotate13)
        self.rotate_button13.place(x=700, y=yval)
        self.buttons.append(self.rotate_button13)
        yval += 30

        #Button 14 - Top Row Counterclockwise
        self.rotate_button14 = Button(self.root, text="Yellow Top Counterclockwise", command=self.rotate14)
        self.rotate_button14.place(x=700, y=yval)
        self.buttons.append(self.rotate_button14)
        yval += 30

        #Button 15 - Second Row Clockwise
        self.rotate_button15 = Button(self.root, text="Yellow Second Row Clockwise", command=self.rotate15)
        self.rotate_button15.place(x=700, y=yval)
        self.buttons.append(self.rotate_button15)
        yval += 30

        #Button 16 - Second Row Counterclockwise
        self.rotate_button16 = Button(self.root, text="Yellow Second Row Counterclockwise", command=self.rotate16)
        self.rotate_button16.place(x=700, y=yval)
        self.buttons.append(self.rotate_button16)
        yval += 30

        #Button 17 - Last Row Clockwise
        self.rotate_button17 = Button(self.root, text="Yellow Last Row Clockwise", command=self.rotate17)
        self.rotate_button17.place(x=700, y=yval)
        self.buttons.append(self.rotate_button17)
        yval += 30

        #Button 18 - Last Row Counterclockwise
        self.rotate_button18 = Button(self.root, text="Yellow Last Row Counterclockwise", command=self.rotate18)
        self.rotate_button18.place(x=700, y=yval)
        self.buttons.append(self.rotate_button18)
        yval += 50

        #----------------------- BLUE FACE at the bottom-------------------------------------#
        #Button 19 - Last Row Counterclockwise
        self.rotate_button19 = Button(self.root, text="Blue Top Clockwise", command=self.rotate19)
        self.rotate_button19.place(x=700, y=yval)
        self.buttons.append(self.rotate_button19)
        yval += 30

        #Button 20 - Last Row Counterclockwise
        self.rotate_button20 = Button(self.root, text="Blue Top Counterclockwise", command=self.rotate20)
        self.rotate_button20.place(x=700, y=yval)
        self.buttons.append(self.rotate_button20)
        yval += 30

        #Button 21 - Last Row Counterclockwise
        self.rotate_button21 = Button(self.root, text="Blue SecondRow Clockwise", command=self.rotate21)
        self.rotate_button21.place(x=700, y=yval)
        self.buttons.append(self.rotate_button21)
        yval += 30
        
        #Button 22 - Last Row Counterclockwise
        self.rotate_button22 = Button(self.root, text="Blue SecondRow Counterclockwise", command=self.rotate22)
        self.rotate_button22.place(x=700, y=yval)
        self.buttons.append(self.rotate_button22)
        yval += 30

        #Button 23 - Last Row Counterclockwise
        self.rotate_button23 = Button(self.root, text="Blue Last Row Clockwise", command=self.rotate23)
        self.rotate_button23.place(x=700, y=yval)
        self.buttons.append(self.rotate_button23)
        yval += 30

        #Button 24 - Last Row Counterclockwise
        self.rotate_button24 = Button(self.root, text="Blue Last Row Counterclockwise", command=self.rotate24)
        self.rotate_button24.place(x=700, y=yval)
        self.buttons.append(self.rotate_button24)
        yval += 30
    

    def updateGui(self):
        self.canvas.delete("all")
        self.triangles = []  # Reset the triangle list
        faces = self.pyraminx.faces

        # Example of drawing the 'A' face at position (300, 200)
         ## RED (middle)
        red_face = faces['A']
        self.draw_face(300, 60, red_face, "red")

        ## GREEN (left)
        green_face = faces['B']
        self.draw_face(100, 60, green_face, "green")

        ## YELLOW (right)
        yellow_face = faces['D']
        self.draw_face(500, 60, yellow_face, "yellow")

        ## BLUE (bottom)
        blue_face = faces['C']
        self.draw_face(260, 280, blue_face, "blue")

    def draw_face(self, x, y, face, default_color):
        size = 20
        for i in range(4):  # Loop through rows
            for j in range(i + 1):  # Loop through each triangle in the row
                # Calculate position
                x_pos = x + (j * 40) - (i * 20)
                y_pos = y + (i * 40)
                color = face[i][j] if face[i][j] else default_color
                
                # Draw the right-side-up triangle
                self.draw_triangle(x_pos, y_pos, color, PyraminxGui.triangle_id)
                
                # Label for the right-side-up triangle
                self.canvas.create_text(x_pos, y_pos + 10, text=f"{PyraminxGui.triangle_id}", fill="black", font=('Arial', 8))
                
                # Save information about the triangle
                self.triangles.append({
                    "id": PyraminxGui.triangle_id,
                    "row": i,
                    "col": j,
                    "type": "normal",
                    "x": x_pos,
                    "y": y_pos,
                    "color": color
                })
                PyraminxGui.triangle_id += 1

                # Draw the upside-down triangle except for the last triangle in the row
                if j != i:
                    x_pos_ud = x + (j * 40) - (i * 20) + size
                    self.draw_upsidedown_triangle(x_pos_ud, y_pos, color, PyraminxGui.triangle_id)

                    # Label for the upside-down triangle
                    self.canvas.create_text(x_pos_ud, y_pos, text=f"{PyraminxGui.triangle_id}", fill="black", font=('Arial', 8), anchor='center')

                    
                    # Save information about the upside-down triangle
                    self.triangles.append({
                        "id": PyraminxGui.triangle_id,
                        "row": i,
                        "col": j,
                        "type": "upside-down",
                        "x": x_pos_ud,
                        "y": y_pos,
                        "color": color
                    })
                    PyraminxGui.triangle_id += 1

    def draw_triangle(self, x, y, color, triangle_id):
        size = 20
        x1 = x
        x2 = x - size
        x3 = x + size
        y1 = y - size
        y2 = y + size
        y3 = y + size
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black', tags=f"triangle_{triangle_id}")

    def draw_upsidedown_triangle(self, x, y, color, triangle_id):
        size = 20
        x1 = x
        x2 = x - size
        x3 = x + size
        y1 = y + size
        y2 = y - size
        y3 = y - size
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black', tags=f"triangle_{triangle_id}")

        
    def randomize_puzzle(self):
        self.button.config(state=DISABLED)
        global num_moves

        # Randomize the puzzle 
        try:
            num_moves = int(self.input_moves.get())

            self.randomize(num_moves)
            self.calc_heuristic()

        except ValueError:
            print("Please enter a valid number")
    
    # K random moves (num_moves)
    def randomize(self, num_moves):

        # List of all the clockwise functions
        rotations = [
            self.rotate1, self.rotate3, self.rotate5, self.rotate7,
            self.rotate9, self.rotate11, self.rotate13, self.rotate15,
            self.rotate17, self.rotate19, self.rotate21, self.rotate23
        ]

        for _ in range(num_moves):
            random.choice(rotations)()

    def reset_puzzle(self):
        self.button.config(state=NORMAL)
        # Manually set colors for each triangle ID
        for triangle in self.triangles:
            triangle_id = triangle['id']
            if 0 <= triangle_id <= 15:
                triangle['color'] = 'red'     # IDs 0-15 are red
            elif 16 <= triangle_id <= 31:
                triangle['color'] = 'green'   # IDs 16-31 are green
            elif 32 <= triangle_id <= 47:
                triangle['color'] = 'yellow'   # IDs 32-47 are yellow
            elif 48 <= triangle_id <= 63:
                triangle['color'] = 'blue'     # IDs 48-63 are blue

        # Update the canvas to reflect the new colors for all triangles
        for triangle in range(len(self.triangles)):  # Update for all triangles
            self.update_triangle_color(triangle)



    def update_triangle_color(self, triangle_id):
        # Update the color of the triangle with the specified ID on the canvas
        triangle = self.triangles[triangle_id]
        self.canvas.itemconfig(f"triangle_{triangle_id}", fill=triangle['color'])
    

#--------------------- SOLVING ----------------------------------#
    
    # Admissible Heuristic is the max number of colors on any face minus 1, range is 0-3
    def calc_heuristic(self):
        # Define the triangle IDs for each face of the Pyraminx
        faces = [
            [0, 1, 2, 3, 4, 5, 6, 7],  # Example IDs for one face
            [8, 9, 10, 11, 12, 13, 14, 15],  # Another face
            [16, 17, 18, 19, 20, 21, 22, 23],  # And so on
            [24, 25, 26, 27, 28, 29, 30, 31],
            [32, 33, 34, 35, 36, 37, 38, 39],
            [40, 41, 42, 43, 44, 45, 46, 47],
            [48, 49, 50, 51, 52, 53, 54, 55],
            [56, 57, 58, 59, 60, 61, 62, 63]
        ]
        
        max_colors_on_face = 0
        
        # Loop through each face and count the number of unique colors
        for face in faces:
            colors_on_face = set(self.triangles[triangle_id]['color'] for triangle_id in face)
            max_colors_on_face = max(max_colors_on_face, len(colors_on_face))
        
        # The heuristic is max number of unique colors on any face - 1
        heuristic = max_colors_on_face - 1
        print(f"Heuristic:", (heuristic))
        return heuristic


    def solve(self):
        open_list = []      # List for the open states (priority queue)
        closed_list = set() # Set for visited states
        parent_map = {}
        history = []

        initial_cost = 0
        initial_state = self.get_current_state()
        initial_heuristic = self.calc_heuristic()

        # Mapping each rotation function to a move name
        counter_rotations = [
            (self.rotate2, 'rotate2'), (self.rotate4, 'rotate4'), 
            (self.rotate6, 'rotate6'), (self.rotate8, 'rotate8'), 
            (self.rotate10, 'rotate10'), (self.rotate12, 'rotate12'),
            (self.rotate14, 'rotate14'), (self.rotate16, 'rotate16'),
            (self.rotate18, 'rotate18'), (self.rotate20, 'rotate20'),
            (self.rotate22, 'rotate22'), (self.rotate24, 'rotate24')
    ]

        # Push the initial state onto the open list with its cost
        # f(n) = g(n) + h(n), intial cost is the cost to reach the current state from initial state
        # This is the first step, meaning initial cost is 0 + heuristic value: (0 + x, 0, initial_state)
        heapq.heappush(open_list, (initial_cost + initial_heuristic, initial_cost, initial_state))
        parent_map[tuple(map(tuple, initial_state))] = None

        while open_list:
            current_cost, g_n, current_state = heapq.heappop(open_list)
            history.append(current_state)

            # Check if the current state is the goal state
            if self.is_goal_state(current_state):
                print("Solved!!")
                return self.reconstruct_path(history, current_state)
            
            # Add the current state to the closed list
            closed_list.add(tuple(map(tuple, current_state)))

            # Expand the current state to get neighbors
            for move, move_name in counter_rotations:
                next_state = self.copy_state(current_state)

                move()
                print(f"Applying move: {move_name}")
                    # Check if apply_move returned None
                if next_state is None:
                    print(f"Move {move} did not produce a valid state.")
                    continue  # Skip this move if it didn't produce a valid state
                # Check if the new state has already been visited
                if tuple(map(tuple, next_state)) in closed_list:
                    continue

                nextg_n = g_n + 1
                next_heuristic = self.calc_heuristic(next_state)
                heapq.heappush(open_list, (nextg_n + next_heuristic, nextg_n, next_state))
                parent_map[tuple(map(tuple, next_state))] = current_state

        print("No solution found.")
        return None


    
    def is_goal_state(self, state):
        solved_state = {
            'A': [['red'] * 4 for _ in range(4)],  # Red face
            'B': [['green'] * 4 for _ in range(4)],  # Green face
            'C': [['yellow'] * 4 for _ in range(4)],  # Blue face
            'D': [['blue'] * 4 for _ in range(4)]  # Yellow face
        }

        # Check if the current state matches the solved state
        return state == solved_state

    def copy_state(self, state):
        # Return a deep copy of the state
        return [list(row) for row in state]  # Adjust this based on your state structure

    def reconstruct_path(self, history, goal_state):
        # Find the index of the goal state in the history
        for state in history:
            # Check if current state is the goal state
            if self.is_goal_state(state):
                # Return path from start to goal
                return history[:history.index(state) + 1]
                
        return [] # Return empty is no path found

    def get_current_state(self):
        # Initialize the dictionary for faces
        color_dict = {
            'A': [[None] * 4 for _ in range(4)],
            'B': [[None] * 4 for _ in range(4)],
            'C': [[None] * 4 for _ in range(4)],
            'D': [[None] * 4 for _ in range(4)],
        }

        # Triangle face mapping
        triangle_face_mapping = {
        # Face A (red)
        0: ('A', 0, 0), 1: ('A', 0, 1), 2: ('A', 0, 2), 3: ('A', 0, 3),
        4: ('A', 1, 0), 5: ('A', 1, 1), 6: ('A', 1, 2), 7: ('A', 1, 3),
        8: ('A', 2, 0), 9: ('A', 2, 1), 10: ('A', 2, 2), 11: ('A', 2, 3),
        12: ('A', 3, 0), 13: ('A', 3, 1), 14: ('A', 3, 2), 15: ('A', 3, 3),

        # Face B (green)
        16: ('B', 0, 0), 17: ('B', 0, 1), 18: ('B', 0, 2), 19: ('B', 0, 3),
        20: ('B', 1, 0), 21: ('B', 1, 1), 22: ('B', 1, 2), 23: ('B', 1, 3),
        24: ('B', 2, 0), 25: ('B', 2, 1), 26: ('B', 2, 2), 27: ('B', 2, 3),
        28: ('B', 3, 0), 29: ('B', 3, 1), 30: ('B', 3, 2), 31: ('B', 3, 3),

        # Face C (yellow)
        32: ('C', 0, 0), 33: ('C', 0, 1), 34: ('C', 0, 2), 35: ('C', 0, 3),
        36: ('C', 1, 0), 37: ('C', 1, 1), 38: ('C', 1, 2), 39: ('C', 1, 3),
        40: ('C', 2, 0), 41: ('C', 2, 1), 42: ('C', 2, 2), 43: ('C', 2, 3),
        44: ('C', 3, 0), 45: ('C', 3, 1), 46: ('C', 3, 2), 47: ('C', 3, 3),

        # Face D (blue)
        48: ('D', 0, 0), 49: ('D', 0, 1), 50: ('D', 0, 2), 51: ('D', 0, 3),
        52: ('D', 1, 0), 53: ('D', 1, 1), 54: ('D', 1, 2), 55: ('D', 1, 3),
        56: ('D', 2, 0), 57: ('D', 2, 1), 58: ('D', 2, 2), 59: ('D', 2, 3),
        60: ('D', 3, 0), 61: ('D', 3, 1), 62: ('D', 3, 2), 63: ('D', 3, 3),

        }
        # Populate the dictionary with colors based on triangle IDs
        for triangle in self.triangles:
            triangle_id = triangle['id']
            color = triangle['color']
            
            # Check if the triangle ID is in the mapping
            if triangle_id in triangle_face_mapping:
                face, row, col = triangle_face_mapping[triangle_id]
                color_dict[face][row][col] = color
        return color_dict


    








#--------------------- ROTATIONS --------------------------------#
    ##---------------- RED on bottom -----------------------##
    # Red clockwise rotation

    # Red counterclockwise rotation
    def rotate1(self):
         # Access the colors of the triangles with the specified IDs
        color2 = self.triangles[16]['color']
        color3 = self.triangles[47]['color']
        color4 = self.triangles[57]['color']

        # Perform a color swap in a circular manner
        self.triangles[16]['color'] = color4
        self.triangles[47]['color'] = color2
        self.triangles[57]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [16, 47, 57]:
            self.update_triangle_color(triangle)
         
    def rotate2(self):
        # Access the colors of the triangles with the specified IDs
        color2 = self.triangles[16]['color']
        color3 = self.triangles[47]['color']
        color4 = self.triangles[57]['color']

        # Perform a color swap in a circular manner 
        self.triangles[16]['color'] = color3
        self.triangles[47]['color'] = color4
        self.triangles[57]['color'] = color2

        # Update the canvas to reflect the new colors
        for triangle in [16, 47, 57]:
            self.update_triangle_color(triangle)
    

    def rotate3(self):
        # Red second row counterclockwise rotation

        color1 = self.triangles[17]['color']
        color2 = self.triangles[18]['color']
        color3 = self.triangles[19]['color']

        color4 = self.triangles[40]['color']
        color5 = self.triangles[46]['color']
        color6 = self.triangles[45]['color']

        color7 = self.triangles[52]['color']
        color8 = self.triangles[58]['color']
        color9 = self.triangles[59]['color']

        # Swap
        self.triangles[17]['color'] = color7
        self.triangles[18]['color'] = color8
        self.triangles[19]['color'] = color9
        self.triangles[40]['color'] = color1
        self.triangles[46]['color'] = color2
        self.triangles[45]['color'] = color3
        self.triangles[52]['color'] = color4
        self.triangles[58]['color'] = color5
        self.triangles[59]['color'] = color6

        # Update the canvas to reflect the new colors
        for triangle in [52, 58, 59, 17, 18, 19, 40, 46, 45]:
            self.update_triangle_color(triangle)
    # Red second row clockwise rotation
    def rotate4(self):

        color1 = self.triangles[17]['color']
        color2 = self.triangles[18]['color']
        color3 = self.triangles[19]['color']

        color4 = self.triangles[40]['color']
        color5 = self.triangles[46]['color']
        color6 = self.triangles[45]['color']

        color7 = self.triangles[52]['color']
        color8 = self.triangles[58]['color']
        color9 = self.triangles[59]['color']

        self.triangles[52]['color'] = color1
        self.triangles[58]['color'] = color2
        self.triangles[59]['color'] = color3
        self.triangles[17]['color'] = color4
        self.triangles[18]['color'] = color5
        self.triangles[19]['color'] = color6
        self.triangles[40]['color'] = color7
        self.triangles[46]['color'] = color8
        self.triangles[45]['color'] = color9

        # Update the canvas to reflect the new colors
        for triangle in [52, 58, 59, 17, 18, 19, 40, 46, 45]:
            self.update_triangle_color(triangle)

    def rotate5(self):
        # Red last row counterclockwise rotation

        color1 = self.triangles[25]['color']
        color2 = self.triangles[26]['color']
        color3 = self.triangles[27]['color']
        color4 = self.triangles[28]['color']
        color5 = self.triangles[29]['color']
        color6 = self.triangles[30]['color']
        color7 = self.triangles[31]['color']

        color8 = self.triangles[32]['color']
        color9 = self.triangles[34]['color']
        color10 = self.triangles[33]['color']
        color11 = self.triangles[37]['color']
        color12 = self.triangles[36]['color']
        color13 = self.triangles[42]['color']
        color14 = self.triangles[41]['color']

        color15 = self.triangles[48]['color']
        color16 = self.triangles[50]['color']
        color17 = self.triangles[51]['color']
        color18 = self.triangles[55]['color']
        color19 = self.triangles[56]['color']
        color20 = self.triangles[62]['color']
        color21 = self.triangles[63]['color']

        # Swap in reverse (clockwise)
        self.triangles[25]['color'] = color15
        self.triangles[26]['color'] = color16
        self.triangles[27]['color'] = color17
        self.triangles[28]['color'] = color18
        self.triangles[29]['color'] = color19
        self.triangles[30]['color'] = color20
        self.triangles[31]['color'] = color21

        self.triangles[32]['color'] = color1
        self.triangles[34]['color'] = color2
        self.triangles[33]['color'] = color3
        self.triangles[37]['color'] = color4
        self.triangles[36]['color'] = color5
        self.triangles[42]['color'] = color6
        self.triangles[41]['color'] = color7

        self.triangles[48]['color'] = color8
        self.triangles[50]['color'] = color9
        self.triangles[51]['color'] = color10
        self.triangles[55]['color'] = color11
        self.triangles[56]['color'] = color12
        self.triangles[62]['color'] = color13
        self.triangles[63]['color'] = color14

        # Update the canvas to reflect the new colors
        for triangle in [25, 26, 27, 28, 29, 30, 31, 32, 34, 33, 37, 36, 42, 41, 48, 50, 51, 55, 56, 62, 63]:
            self.update_triangle_color(triangle)
    
    def rotate6(self):
        # Red last row clockwise rotation

        color1 = self.triangles[25]['color']
        color2 = self.triangles[26]['color']
        color3 = self.triangles[27]['color']
        color4 = self.triangles[28]['color']
        color5 = self.triangles[29]['color']
        color6 = self.triangles[30]['color']
        color7 = self.triangles[31]['color']

        color8 = self.triangles[32]['color']
        color9 = self.triangles[34]['color']
        color10 = self.triangles[33]['color']
        color11 = self.triangles[37]['color']
        color12 = self.triangles[36]['color']
        color13 = self.triangles[42]['color']
        color14 = self.triangles[41]['color']

        color15 = self.triangles[48]['color']
        color16 = self.triangles[50]['color']
        color17= self.triangles[51]['color']
        color18 = self.triangles[55]['color']
        color19 = self.triangles[56]['color']
        color20 = self.triangles[62]['color']
        color21 = self.triangles[63]['color']

        # Swap
        self.triangles[25]['color'] = color8
        self.triangles[26]['color'] = color9
        self.triangles[27]['color'] = color10
        self.triangles[28]['color'] = color11
        self.triangles[29]['color'] = color12
        self.triangles[30]['color'] = color13
        self.triangles[31]['color'] = color14

        self.triangles[32]['color'] = color15
        self.triangles[34]['color'] = color16
        self.triangles[33]['color'] = color17
        self.triangles[37]['color'] = color18
        self.triangles[36]['color'] = color19
        self.triangles[42]['color'] = color20
        self.triangles[41]['color'] = color21

        self.triangles[48]['color'] = color1
        self.triangles[50]['color'] = color2
        self.triangles[51]['color'] = color3
        self.triangles[55]['color'] = color4
        self.triangles[56]['color'] = color5
        self.triangles[62]['color'] = color6
        self.triangles[63]['color'] = color7


        # Update the canvas to reflect the new colors
        for triangle in [25, 26, 27, 28, 29, 30, 31, 32, 34, 33, 37, 36, 42, 41, 48, 50, 51, 55, 56, 62, 63]:
            self.update_triangle_color(triangle)
        

    ##---------------- GREEN on bottom -----------------------##
    def rotate7(self):
        # Top clockwise
        
        color2 = self.triangles[15]['color']    #Red
        color3 = self.triangles[41]['color']    #Yellow
        color4 = self.triangles[63]['color']    #Blue 

        # Perform a color swap in a circular manner 
        self.triangles[15]['color'] = color4
        self.triangles[41]['color'] = color2
        self.triangles[63]['color'] = color3

         # Update the canvas to reflect the new colors
        for triangle in [15, 41, 63]:
            self.update_triangle_color(triangle)
    
    def rotate8(self):
        # Top counterclockwise
        color2 = self.triangles[15]['color']
        color3 = self.triangles[41]['color']
        color4 = self.triangles[63]['color']

        # Perform a color swap in the opposite (counterclockwise) direction
        self.triangles[15]['color'] = color3
        self.triangles[41]['color'] = color4
        self.triangles[63]['color'] = color2

        # Update the canvas to reflect the new colors
        for triangle in [15,41,63]:
            self.update_triangle_color(triangle)
    
    def rotate9(self):
        color1 = self.triangles[8]['color']
        color2 = self.triangles[14]['color']
        color3 = self.triangles[13]['color']

        color4 = self.triangles[36]['color']
        color5 = self.triangles[42]['color']
        color6 = self.triangles[43]['color']

        color7 = self.triangles[56]['color']
        color8 = self.triangles[62]['color']
        color9 = self.triangles[61]['color']

        # Perform the counterclockwise rotation of the colors
        self.triangles[8]['color'] = color7
        self.triangles[14]['color'] = color8
        self.triangles[13]['color'] = color9

        self.triangles[36]['color'] = color1
        self.triangles[42]['color'] = color2
        self.triangles[43]['color'] = color3

        self.triangles[61]['color'] = color4
        self.triangles[62]['color'] = color5
        self.triangles[56]['color'] = color6

        # Update the canvas to reflect the new colors
        for triangle in [8, 14, 13, 36, 42, 43, 56, 62, 61]:
            self.update_triangle_color(triangle)
        
    def rotate10(self):
        color1 = self.triangles[8]['color']
        color2 = self.triangles[14]['color']
        color3 = self.triangles[13]['color']

        color4 = self.triangles[36]['color']
        color5 = self.triangles[42]['color']
        color6 = self.triangles[43]['color']

        color7 = self.triangles[61]['color']
        color8 = self.triangles[62]['color']
        color9 = self.triangles[56]['color']

        # Perform the counterclockwise rotation of the colors
        self.triangles[8]['color'] = color4
        self.triangles[14]['color'] = color5
        self.triangles[13]['color'] = color6

        self.triangles[36]['color'] = color7
        self.triangles[42]['color'] = color8
        self.triangles[43]['color'] = color9

        self.triangles[56]['color'] = color1
        self.triangles[62]['color'] = color2
        self.triangles[61]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [8, 14, 13, 36, 42, 43, 56, 62, 61]:
            self.update_triangle_color(triangle)

    def rotate11(self):
        # Access the colors of the triangles with the specified IDs
        color1 = self.triangles[0]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[1]['color']
        color4 = self.triangles[5]['color']
        color5 = self.triangles[4]['color']
        color6 = self.triangles[10]['color']
        color7 = self.triangles[9]['color']

        color8 = self.triangles[48]['color']
        color9 = self.triangles[50]['color']
        color10 = self.triangles[49]['color']
        color11 = self.triangles[53]['color']
        color12 = self.triangles[52]['color']
        color13 = self.triangles[58]['color']
        color14 = self.triangles[57]['color']

        color15 = self.triangles[32]['color']
        color16 = self.triangles[34]['color']
        color17 = self.triangles[35]['color']
        color18 = self.triangles[39]['color']
        color19 = self.triangles[40]['color']
        color20 = self.triangles[46]['color']
        color21 = self.triangles[47]['color']

        # Perform the reversed (counterclockwise) rotation of the colors
        self.triangles[0]['color'] = color8
        self.triangles[2]['color'] = color9
        self.triangles[1]['color'] = color10
        self.triangles[5]['color'] = color11
        self.triangles[4]['color'] = color12
        self.triangles[10]['color'] = color13
        self.triangles[9]['color'] = color14

        self.triangles[48]['color'] = color15
        self.triangles[50]['color'] = color16
        self.triangles[52]['color'] = color17
        self.triangles[53]['color'] = color18
        self.triangles[49]['color'] = color19
        self.triangles[58]['color'] = color20
        self.triangles[57]['color'] = color21

        # Third group -> First group
        self.triangles[32]['color'] = color1
        self.triangles[34]['color'] = color2
        self.triangles[35]['color'] = color3
        self.triangles[39]['color'] = color4
        self.triangles[40]['color'] = color5
        self.triangles[46]['color'] = color6
        self.triangles[47]['color'] = color7

        # Update the canvas to reflect the new colors
        for triangle in [0, 1, 2, 5, 4, 10, 9, 48, 50, 49, 53, 52, 58, 57, 32, 34, 35, 39, 40, 46, 47]:
            self.update_triangle_color(triangle)

    def rotate12(self):
        # Access the colors of the triangles with the specified IDs
        color1 = self.triangles[0]['color']
        color2 = self.triangles[1]['color']
        color3 = self.triangles[2]['color']
        color4 = self.triangles[5]['color']
        color5 = self.triangles[4]['color']
        color6 = self.triangles[10]['color']
        color7 = self.triangles[9]['color']

        color8 = self.triangles[48]['color']
        color9 = self.triangles[50]['color']
        color10 = self.triangles[49]['color']
        color11 = self.triangles[53]['color']
        color12 = self.triangles[52]['color']
        color13 = self.triangles[58]['color']
        color14 = self.triangles[57]['color']

        color15 = self.triangles[32]['color']
        color16 = self.triangles[34]['color']
        color17 = self.triangles[35]['color']
        color18 = self.triangles[39]['color']
        color19 = self.triangles[40]['color']
        color20 = self.triangles[46]['color']
        color21 = self.triangles[47]['color']

        # Swaps
        self.triangles[0]['color'] = color15
        self.triangles[1]['color'] = color16
        self.triangles[2]['color'] = color17
        self.triangles[5]['color'] = color18
        self.triangles[4]['color'] = color19
        self.triangles[10]['color'] = color20
        self.triangles[9]['color'] = color21

        self.triangles[48]['color'] = color1
        self.triangles[50]['color'] = color2
        self.triangles[49]['color'] = color3
        self.triangles[53]['color'] = color4
        self.triangles[52]['color'] = color5
        self.triangles[58]['color'] = color6
        self.triangles[57]['color'] = color7

        # Third group -> First group
        self.triangles[32]['color'] = color8
        self.triangles[34]['color'] = color9
        self.triangles[35]['color'] = color10
        self.triangles[39]['color'] = color11
        self.triangles[40]['color'] = color12
        self.triangles[46]['color'] = color13
        self.triangles[47]['color'] = color14

        # Update the canvas to reflect the new colors
        for triangle in [0, 1, 2, 5, 4, 10, 9, 48, 50, 49, 53, 52, 58, 57, 32, 34, 35, 39, 40, 46, 47]:
            self.update_triangle_color(triangle)

    




    #----------------------- YELLOW on bottom ------------------------#
    def rotate13(self):
        # Top clockwise
        
        color2 = self.triangles[9]['color']    #Red
        color3 = self.triangles[25]['color']    #Yellow
        color4 = self.triangles[48]['color']    #Blue 

        # Perform a color swap in a circular manner 
        self.triangles[9]['color'] = color3
        self.triangles[25]['color'] = color4
        self.triangles[48]['color'] = color2

         # Update the canvas to reflect the new colors
        for triangle in [9, 25, 48]:
            self.update_triangle_color(triangle)
    
    def rotate14(self):
        # Top clockwise
        
        color2 = self.triangles[9]['color']    #Red
        color3 = self.triangles[25]['color']    #Yellow
        color4 = self.triangles[48]['color']    #Blue 

        # Perform a color swap in a circular manner 
        self.triangles[9]['color'] = color4
        self.triangles[25]['color'] = color2
        self.triangles[48]['color'] = color3

         # Update the canvas to reflect the new colors
        for triangle in [9, 25, 48]:
            self.update_triangle_color(triangle)

    #Second Row Rotation
    def rotate15(self):
        color1 = self.triangles[11]['color']
        color2 = self.triangles[10]['color']
        color3 = self.triangles[4]['color']

        color4 = self.triangles[27]['color']
        color5 = self.triangles[26]['color']
        color6 = self.triangles[20]['color']

        color7 = self.triangles[49]['color']
        color8 = self.triangles[50]['color']
        color9 = self.triangles[51]['color']

        # Perform the counterclockwise rotation of the colors
        self.triangles[11]['color'] = color4
        self.triangles[10]['color'] = color5
        self.triangles[4]['color'] = color6

        self.triangles[27]['color'] = color7
        self.triangles[26]['color'] = color8
        self.triangles[20]['color'] = color9

        self.triangles[49]['color'] = color1
        self.triangles[50]['color'] = color2
        self.triangles[51]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [4, 10, 11, 20, 26, 27, 49, 50, 51]:
            self.update_triangle_color(triangle)

    def rotate16(self):
        color1 = self.triangles[11]['color']
        color2 = self.triangles[10]['color']
        color3 = self.triangles[4]['color']

        color4 = self.triangles[27]['color']
        color5 = self.triangles[26]['color']
        color6 = self.triangles[20]['color']

        color7 = self.triangles[51]['color']
        color8 = self.triangles[50]['color']
        color9 = self.triangles[49]['color']

        # Perform the clockwise rotation of the colors
        self.triangles[11]['color'] = color7
        self.triangles[10]['color'] = color8
        self.triangles[4]['color'] = color9

        self.triangles[27]['color'] = color1
        self.triangles[26]['color'] = color2
        self.triangles[20]['color'] = color3

        self.triangles[51]['color'] = color4
        self.triangles[50]['color'] = color5
        self.triangles[49]['color'] = color6

        # Update the canvas to reflect the new colors
        for triangle in [4, 10, 11, 20, 26, 27, 49, 50, 51]:
            self.update_triangle_color(triangle)

    def rotate17(self):
        # New rotation with specified triangle IDs

        # First group: 0, 2, 3, 7, 8, 14, 15
        color1 = self.triangles[0]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[3]['color']
        color4 = self.triangles[7]['color']
        color5 = self.triangles[8]['color']
        color6 = self.triangles[14]['color']
        color7 = self.triangles[15]['color']

        # Second group: 16, 18, 19, 23, 24, 30, 31
        color8 = self.triangles[16]['color']
        color9 = self.triangles[18]['color']
        color10 = self.triangles[19]['color']
        color11 = self.triangles[23]['color']
        color12 = self.triangles[24]['color']
        color13 = self.triangles[30]['color']
        color14 = self.triangles[31]['color']

        # Third group: 57, 58, 59, 60, 61, 62, 63
        color15 = self.triangles[57]['color']
        color16 = self.triangles[58]['color']
        color17 = self.triangles[61]['color']
        color18 = self.triangles[60]['color']
        color19 = self.triangles[59]['color']
        color20 = self.triangles[62]['color']
        color21 = self.triangles[63]['color']

        # Perform the reverse swap (clockwise rotation)
        # Third group -> First group
        self.triangles[0]['color'] = color8
        self.triangles[2]['color'] = color9
        self.triangles[3]['color'] = color10
        self.triangles[7]['color'] = color11
        self.triangles[8]['color'] = color12
        self.triangles[14]['color'] = color13
        self.triangles[15]['color'] = color14

        # First group -> Second group
        self.triangles[16]['color'] = color15
        self.triangles[18]['color'] = color16
        self.triangles[19]['color'] = color17
        self.triangles[23]['color'] = color18
        self.triangles[24]['color'] = color19
        self.triangles[30]['color'] = color20
        self.triangles[31]['color'] = color21

        # Second group -> Third group
        self.triangles[57]['color'] = color1
        self.triangles[58]['color'] = color2
        self.triangles[61]['color'] = color3
        self.triangles[60]['color'] = color4
        self.triangles[59]['color'] = color5
        self.triangles[62]['color'] = color6
        self.triangles[63]['color'] = color7

        # Update the canvas to reflect the new colors
        for triangle in [0, 2, 3, 7, 8, 14, 15, 16, 18, 19, 23, 24, 30, 31, 57, 58, 59, 60, 61, 62, 63]:
            self.update_triangle_color(triangle)


    def rotate18(self):
        color1 = self.triangles[0]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[3]['color']
        color4 = self.triangles[7]['color']
        color5 = self.triangles[8]['color']
        color6 = self.triangles[14]['color']
        color7 = self.triangles[15]['color']

        color8 = self.triangles[16]['color']
        color9 = self.triangles[18]['color']
        color10 = self.triangles[19]['color']
        color11 = self.triangles[23]['color']
        color12 = self.triangles[24]['color']
        color13 = self.triangles[30]['color']
        color14 = self.triangles[31]['color']

        color15 = self.triangles[57]['color']
        color16 = self.triangles[58]['color']
        color17 = self.triangles[59]['color']
        color18 = self.triangles[60]['color']
        color19 = self.triangles[61]['color']
        color20 = self.triangles[62]['color']
        color21 = self.triangles[63]['color']

        # Swaps
        self.triangles[0]['color'] = color15
        self.triangles[2]['color'] = color16
        self.triangles[3]['color'] = color17
        self.triangles[7]['color'] = color18
        self.triangles[8]['color'] = color19
        self.triangles[14]['color'] = color20
        self.triangles[15]['color'] = color21

        self.triangles[16]['color'] = color1
        self.triangles[18]['color'] = color2
        self.triangles[19]['color'] = color3
        self.triangles[23]['color'] = color4
        self.triangles[24]['color'] = color5
        self.triangles[30]['color'] = color6
        self.triangles[31]['color'] = color7

        # Third group -> First group
        self.triangles[57]['color'] = color8
        self.triangles[58]['color'] = color9
        self.triangles[61]['color'] = color10
        self.triangles[60]['color'] = color11
        self.triangles[59]['color'] = color12
        self.triangles[62]['color'] = color13
        self.triangles[63]['color'] = color14

        # Update the canvas to reflect the new colors
        for triangle in [0, 2, 3, 7, 8, 14, 15, 16, 18, 19, 23, 24, 30, 31, 57, 58, 59, 60, 61, 62, 63]:
            self.update_triangle_color(triangle)

   #------------------- BLUE on bottom ---------------------------#
    def rotate19(self):
        # Blue Top - Clockwise
        color1 = self.triangles[0]['color']
        color2 = self.triangles[31]['color']
        color3 = self.triangles[32]['color']

        self.triangles[0]['color'] = color3
        self.triangles[31]['color'] = color1
        self.triangles[32]['color'] = color2

        for triangle in [0, 31, 32]:
            self.update_triangle_color(triangle)

    def rotate20(self):
        # Blue Top - Counterclockwise
        color1 = self.triangles[0]['color']
        color2 = self.triangles[31]['color']
        color3 = self.triangles[32]['color']

        self.triangles[0]['color'] = color2
        self.triangles[31]['color'] = color3
        self.triangles[32]['color'] = color1

        for triangle in [0, 31, 32]:
            self.update_triangle_color(triangle)

    def rotate21(self):
        # Blue Second - Clockwise
        color1 = self.triangles[1]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[3]['color']
        color4 = self.triangles[24]['color']
        color5 = self.triangles[30]['color']
        color6 = self.triangles[29]['color']
        color7 = self.triangles[33]['color']
        color8 = self.triangles[34]['color']
        color9 = self.triangles[35]['color']

        self.triangles[1]['color'] = color7
        self.triangles[2]['color'] = color8
        self.triangles[3]['color'] = color9
        self.triangles[24]['color'] = color1
        self.triangles[30]['color'] = color2
        self.triangles[29]['color'] = color3
        self.triangles[33]['color'] = color4
        self.triangles[34]['color'] = color5
        self.triangles[35]['color'] = color6

        for triangle in [1, 2, 3, 24, 30, 29, 33, 34, 35]:
            self.update_triangle_color(triangle)

    def rotate22(self):
        # Blue Second - Counterclockwise
        color1 = self.triangles[1]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[3]['color']
        color4 = self.triangles[24]['color']
        color5 = self.triangles[30]['color']
        color6 = self.triangles[29]['color']
        color7 = self.triangles[33]['color']
        color8 = self.triangles[34]['color']
        color9 = self.triangles[35]['color']

        self.triangles[1]['color'] = color4
        self.triangles[2]['color'] = color5
        self.triangles[3]['color'] = color6
        self.triangles[24]['color'] = color7
        self.triangles[30]['color'] = color8
        self.triangles[29]['color'] = color9
        self.triangles[33]['color'] = color1
        self.triangles[34]['color'] = color2
        self.triangles[35]['color'] = color3

        for triangle in [1, 2, 3, 24, 30, 29, 33, 34, 35]:
            self.update_triangle_color(triangle)

    def rotate23(self):
        # Blue Bottom - Clockwise

        # Get the colors of the specified triangles
        color1 = self.triangles[9]['color']
        color2 = self.triangles[10]['color']
        color3 = self.triangles[11]['color']
        color4 = self.triangles[12]['color']
        color5 = self.triangles[13]['color']
        color6 = self.triangles[14]['color']
        color7 = self.triangles[15]['color']

        color8 = self.triangles[41]['color']
        color9 = self.triangles[43]['color']
        color10 = self.triangles[42]['color']
        color11 = self.triangles[44]['color']
        color12 = self.triangles[45]['color']
        color13 = self.triangles[46]['color']
        color14 = self.triangles[47]['color']

        color15 = self.triangles[16]['color']
        color16 = self.triangles[17]['color']
        color17 = self.triangles[18]['color']
        color18 = self.triangles[21]['color']
        color19 = self.triangles[20]['color']
        color20 = self.triangles[25]['color']
        color21 = self.triangles[26]['color']

        # Perform the clockwise rotation of the colors
        # Move bottom face clockwise
        self.triangles[9]['color'] = color8
        self.triangles[10]['color'] = color9
        self.triangles[11]['color'] = color10
        self.triangles[12]['color'] = color11
        self.triangles[13]['color'] = color12
        self.triangles[14]['color'] = color13
        self.triangles[15]['color'] = color14

        # Move side face to bottom face
        self.triangles[41]['color'] = color15
        self.triangles[43]['color'] = color16
        self.triangles[42]['color'] = color17
        self.triangles[44]['color'] = color18
        self.triangles[45]['color'] = color19
        self.triangles[46]['color'] = color20
        self.triangles[47]['color'] = color21

        # Move original bottom face to side face
        self.triangles[16]['color'] = color1
        self.triangles[17]['color'] = color2
        self.triangles[18]['color'] = color3
        self.triangles[21]['color'] = color4
        self.triangles[20]['color'] = color5
        self.triangles[25]['color'] = color6
        self.triangles[26]['color'] = color7

        # Update the canvas to reflect the new colors
        for triangle in [9, 10, 11, 12, 13, 14, 15, 41, 42, 43, 44, 45, 46, 47, 16, 17, 18, 20, 21, 25, 26]:
            self.update_triangle_color(triangle)

    def rotate24(self):
        # Blue Bottom - Counterclockwise

        # Red
        color1 = self.triangles[9]['color']
        color2 = self.triangles[10]['color']
        color3 = self.triangles[11]['color']
        color4 = self.triangles[12]['color']
        color5 = self.triangles[13]['color']
        color6 = self.triangles[14]['color']
        color7 = self.triangles[15]['color']

        # Yellow
        color8 = self.triangles[41]['color']
        color9 = self.triangles[43]['color']
        color10 = self.triangles[42]['color']
        color11 = self.triangles[44]['color']
        color12 = self.triangles[45]['color']
        color13 = self.triangles[46]['color']
        color14 = self.triangles[47]['color']

        # Green
        color15 = self.triangles[16]['color']
        color16 = self.triangles[18]['color']
        color17 = self.triangles[17]['color']
        color18 = self.triangles[21]['color']
        color19 = self.triangles[20]['color']
        color20 = self.triangles[26]['color']
        color21 = self.triangles[25]['color']

        # Perform the counterclockwise rotation of the colors
        self.triangles[9]['color'] = color15
        self.triangles[10]['color'] = color16
        self.triangles[11]['color'] = color17
        self.triangles[12]['color'] = color18
        self.triangles[13]['color'] = color19
        self.triangles[14]['color'] = color20
        self.triangles[15]['color'] = color21


        self.triangles[16]['color'] = color8
        self.triangles[18]['color'] = color9
        self.triangles[17]['color'] = color10
        self.triangles[21]['color'] = color11
        self.triangles[20]['color'] = color12
        self.triangles[26]['color'] = color13
        self.triangles[25]['color'] = color14

        self.triangles[41]['color'] = color1
        self.triangles[43]['color'] = color2
        self.triangles[42]['color'] = color3
        self.triangles[44]['color'] = color4
        self.triangles[45]['color'] = color5
        self.triangles[46]['color'] = color6
        self.triangles[47]['color'] = color7


        # Update the canvas to reflect the new colors
        for triangle in [9, 10, 11, 12, 13, 14, 15, 41, 42, 43, 44, 45, 46, 47, 16, 18, 17, 21, 20, 26, 25]:
            self.update_triangle_color(triangle)

# ------------------- MAIN -----------------------#
root = Tk()
root.resizable(0, 0)
app = PyraminxGui(root)
root.mainloop()
