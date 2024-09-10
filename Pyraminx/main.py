from tkinter import *
import random

global triangle_id

class Pyraminx:
    def __init__(self):
        # Initialize faces with default colors
        self.faces = {
            'A': [["red"] * 4 for _ in range(4)],
            'B': [["green"] * 4 for _ in range(4)],
            'C': [["blue"] * 4 for _ in range(4)],
            'D': [["yellow"] * 4 for _ in range(4)],
        }

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

    def randomize(self):
        colors = self.get_colors()
        random.shuffle(colors)
        self.set_colors(colors)

class PyraminxGui:
    triangle_id = 0
    def __init__(self, root):
        self.root = root
        self.pyraminx = Pyraminx()
        self.triangles = []  # Store triangle information
        root.title("Pyraminx Puzzle")

        self.canvas = Canvas(root, width=1000, height=1000, bg='white')
        self.canvas.pack()

        self.buttons = []
        yval = 50

        # Create and position the buttons
        self.create_buttons(yval)
        self.updateGui()

    def create_buttons(self, yval):
        # Randomize Button
        self.button = Button(self.root, text="Randomize", command=self.randomize_puzzle)
        self.button.place(x=700, y=yval)  # Place the button at (x=820, y=yval)
        self.buttons.append(self.button)  # Add to the list

        # Increment yval to place the buttons close together
        yval += 30

        #----------------------- RED FACE -------------------------------------#

        #Button 1 - Top Clockwise
        self.rotate_button1 = Button(self.root, text="Red Clockwise", command=lambda: self.rotate1(0, 16, 32, 48))
        self.rotate_button1.place(x=700, y=yval)
        self.buttons.append(self.rotate_button1)
        yval += 30  # Increment yval for the next button

        #Button 2 - Top Counterclockwise
        self.rotate_button2 = Button(self.root, text="Red Counterclockwise", command=lambda: self.rotate2(0, 16, 32, 48))
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

         #----------------------- GREEN FACE -------------------------------------#

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
        self.rotate_button9 = Button(self.root, text="Green Top Counterclockwise", command=self.rotate9)
        self.rotate_button9.place(x=700, y=yval)
        self.buttons.append(self.rotate_button9)
        yval += 30

        #Button 10 - Second Row Counterclockwise

    

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
        # Randomize the puzzle (implementation needed)
        pass

    def update_triangle_color(self, triangle_id):
        # Update the color of the triangle with the specified ID on the canvas
        triangle = self.triangles[triangle_id]
        self.canvas.itemconfig(f"triangle_{triangle_id}", fill=triangle['color'])

#--------------------- ROTATIONS --------------------------------#
    ##---------------- RED -----------------------##
    # Red clockwise rotation
    def rotate1(self, id1, id2, id3, id4):
        # Access the colors of the triangles with the specified IDs
        color2 = self.triangles[id2]['color']
        color3 = self.triangles[id3]['color']
        color4 = self.triangles[id4]['color']

        # Perform a color swap in a circular manner 
        self.triangles[id2]['color'] = color3
        self.triangles[id3]['color'] = color4
        self.triangles[id4]['color'] = color2

        # Update the canvas to reflect the new colors
        for triangle in [id1, id2, id3, id4]:
            self.update_triangle_color(triangle)

    # Red counterclockwise rotation
    def rotate2(self, id1, id2, id3, id4):
         # Access the colors of the triangles with the specified IDs
        color2 = self.triangles[id2]['color']
        color3 = self.triangles[id3]['color']
        color4 = self.triangles[id4]['color']

        # Perform a color swap in a circular manner
        self.triangles[id2]['color'] = color4
        self.triangles[id3]['color'] = color2
        self.triangles[id4]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [id1, id2, id3, id4]:
            self.update_triangle_color(triangle)
    
    # Red second row clockwise rotation
    def rotate3(self):

        color1 = self.triangles[17]['color']
        color2 = self.triangles[18]['color']
        color3 = self.triangles[19]['color']

        color4 = self.triangles[33]['color']
        color5 = self.triangles[34]['color']
        color6 = self.triangles[35]['color']

        color7 = self.triangles[49]['color']
        color8 = self.triangles[50]['color']
        color9 = self.triangles[51]['color']

        self.triangles[49]['color'] = color1
        self.triangles[50]['color'] = color2
        self.triangles[51]['color'] = color3
        self.triangles[17]['color'] = color4
        self.triangles[18]['color'] = color5
        self.triangles[19]['color'] = color6
        self.triangles[33]['color'] = color7
        self.triangles[34]['color'] = color8
        self.triangles[35]['color'] = color9

        # Update the canvas to reflect the new colors
        for triangle in [49, 50, 51, 17, 18, 19, 33, 34, 35]:
            self.update_triangle_color(triangle)

    def rotate4(self):
        # Red second row counterclockwise rotation

        color1 = self.triangles[17]['color']
        color2 = self.triangles[18]['color']
        color3 = self.triangles[19]['color']

        color4 = self.triangles[33]['color']
        color5 = self.triangles[34]['color']
        color6 = self.triangles[35]['color']

        color7 = self.triangles[49]['color']
        color8 = self.triangles[50]['color']
        color9 = self.triangles[51]['color']

        # Swap
        self.triangles[17]['color'] = color7
        self.triangles[18]['color'] = color8
        self.triangles[19]['color'] = color9
        self.triangles[33]['color'] = color1
        self.triangles[34]['color'] = color2
        self.triangles[35]['color'] = color3
        self.triangles[49]['color'] = color4
        self.triangles[50]['color'] = color5
        self.triangles[51]['color'] = color6

        # Update the canvas to reflect the new colors
        for triangle in [49, 50, 51, 17, 18, 19, 33, 34, 35]:
            self.update_triangle_color(triangle)

    def rotate5(self):
        # Red second row clockwise rotation

        color1 = self.triangles[25]['color']
        color2 = self.triangles[26]['color']
        color3 = self.triangles[27]['color']
        color4 = self.triangles[28]['color']
        color5 = self.triangles[29]['color']
        color6 = self.triangles[30]['color']
        color7 = self.triangles[31]['color']

        color8 = self.triangles[41]['color']
        color9 = self.triangles[42]['color']
        color10 = self.triangles[43]['color']
        color11 = self.triangles[44]['color']
        color12 = self.triangles[45]['color']
        color13 = self.triangles[46]['color']
        color14 = self.triangles[47]['color']

        color15 = self.triangles[57]['color']
        color16 = self.triangles[58]['color']
        color17= self.triangles[59]['color']
        color18 = self.triangles[60]['color']
        color19 = self.triangles[61]['color']
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

        self.triangles[41]['color'] = color15
        self.triangles[42]['color'] = color16
        self.triangles[43]['color'] = color17
        self.triangles[44]['color'] = color18
        self.triangles[45]['color'] = color19
        self.triangles[46]['color'] = color20
        self.triangles[47]['color'] = color21

        self.triangles[57]['color'] = color1
        self.triangles[58]['color'] = color2
        self.triangles[59]['color'] = color3
        self.triangles[60]['color'] = color4
        self.triangles[61]['color'] = color5
        self.triangles[62]['color'] = color6
        self.triangles[63]['color'] = color7


        # Update the canvas to reflect the new colors
        for triangle in [25, 26, 27, 28, 29, 30, 31, 41, 42, 43, 44, 45, 46, 47, 57, 58, 59, 60, 61, 62, 63]:
            self.update_triangle_color(triangle)
    def rotate6(self):
        # Red second row counterclockwise rotation

        color1 = self.triangles[25]['color']
        color2 = self.triangles[26]['color']
        color3 = self.triangles[27]['color']
        color4 = self.triangles[28]['color']
        color5 = self.triangles[29]['color']
        color6 = self.triangles[30]['color']
        color7 = self.triangles[31]['color']

        color8 = self.triangles[41]['color']
        color9 = self.triangles[42]['color']
        color10 = self.triangles[43]['color']
        color11 = self.triangles[44]['color']
        color12 = self.triangles[45]['color']
        color13 = self.triangles[46]['color']
        color14 = self.triangles[47]['color']

        color15 = self.triangles[57]['color']
        color16 = self.triangles[58]['color']
        color17 = self.triangles[59]['color']
        color18 = self.triangles[60]['color']
        color19 = self.triangles[61]['color']
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

        self.triangles[41]['color'] = color1
        self.triangles[42]['color'] = color2
        self.triangles[43]['color'] = color3
        self.triangles[44]['color'] = color4
        self.triangles[45]['color'] = color5
        self.triangles[46]['color'] = color6
        self.triangles[47]['color'] = color7

        self.triangles[57]['color'] = color8
        self.triangles[58]['color'] = color9
        self.triangles[59]['color'] = color10
        self.triangles[60]['color'] = color11
        self.triangles[61]['color'] = color12
        self.triangles[62]['color'] = color13
        self.triangles[63]['color'] = color14

        # Update the canvas to reflect the new colors
        for triangle in [25, 26, 27, 28, 29, 30, 31, 41, 42, 43, 44, 45, 46, 47, 57, 58, 59, 60, 61, 62, 63]:
            self.update_triangle_color(triangle)
        

    ##---------------- BLUE -----------------------##
    def rotate7(self):
        # Top clockwise
        
        color2 = self.triangles[0]['color']
        color3 = self.triangles[32]['color']
        color4 = self.triangles[48]['color']

        # Perform a color swap in a circular manner 
        self.triangles[0]['color'] = color3
        self.triangles[32]['color'] = color4
        self.triangles[48]['color'] = color2

         # Update the canvas to reflect the new colors
        for triangle in [0, 32, 48]:
            self.update_triangle_color(triangle)
    
    def rotate8(self):
        # Top counterclockwise
        color2 = self.triangles[0]['color']
        color3 = self.triangles[32]['color']
        color4 = self.triangles[48]['color']

        # Perform a color swap in the opposite (counterclockwise) direction
        self.triangles[0]['color'] = color4
        self.triangles[32]['color'] = color2
        self.triangles[48]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [0, 32, 48]:
            self.update_triangle_color(triangle)


    def rotate9(self):
        # Access the colors of the triangles with the specified IDs
        color1 = self.triangles[1]['color']
        color2 = self.triangles[2]['color']
        color3 = self.triangles[3]['color']

        color4 = self.triangles[33]['color']
        color5 = self.triangles[34]['color']
        color6 = self.triangles[35]['color']

        color7 = self.triangles[49]['color']
        color8 = self.triangles[50]['color']
        color9 = self.triangles[51]['color']

        # Perform the clockwise rotation of the colors
        self.triangles[49]['color'] = color1
        self.triangles[50]['color'] = color2
        self.triangles[51]['color'] = color3

        self.triangles[1]['color'] = color4
        self.triangles[2]['color'] = color5
        self.triangles[3]['color'] = color6

        self.triangles[33]['color'] = color7
        self.triangles[34]['color'] = color8
        self.triangles[35]['color'] = color9

        # Update the canvas to reflect the new colors
        for triangle in [1, 2, 3, 33, 34, 35, 49, 50, 51]:
            self.update_triangle_color(triangle)

















# ------------------- MAIN -----------------------#
root = Tk()
root.resizable(0, 0)
app = PyraminxGui(root)
root.mainloop()
