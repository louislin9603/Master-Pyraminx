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

        self.canvas = Canvas(root, width=800, height=800, bg='white')
        self.canvas.pack()

        self.button = Button(root, text="Randomize", command=self.randomize_puzzle)
        self.button.pack()

        # Top rotations
        self.rotate_button1 = Button(root, text="Rotate", command=lambda: self.rotate1(0, 16,32,48))
        self.rotate_button2 = Button(root, text="Rotate2", command=lambda: self.rotate2(0, 16,32,48))
        
        self.rotate_button1.pack()
        self.rotate_button2.pack()

        self.updateGui()

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
                self.canvas.create_text(x_pos, y_pos - 10, text=f"{i},{j}", fill="black", font=('Arial', 8))
                self.canvas.create_text(x_pos, y_pos + 10, text=f"ID: {PyraminxGui.triangle_id}", fill="black", font=('Arial', 8))
                
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
                    self.canvas.create_text(x_pos_ud, y_pos - 10, text=f"{i},{j}", fill="black", font=('Arial', 8))
                    self.canvas.create_text(x_pos_ud, y_pos + 10, text=f"ID: {PyraminxGui.triangle_id}", fill="black", font=('Arial', 8))
                    
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

#--------------------- ROTATIONS --------------------------------#
    # Clockwise rotation
    def rotate1(self, id1, id2, id3, id4):
        # Access the colors of the triangles with the specified IDs
        color1 = self.triangles[id1]['color']
        color2 = self.triangles[id2]['color']
        color3 = self.triangles[id3]['color']
        color4 = self.triangles[id4]['color']

        # Perform a color swap in a circular manner
        self.triangles[id1]['color'] = color4
        self.triangles[id2]['color'] = color1
        self.triangles[id3]['color'] = color2
        self.triangles[id4]['color'] = color3

        # Update the canvas to reflect the new colors
        for triangle in [id1, id2, id3, id4]:
            self.update_triangle_color(triangle)

    # Counterclockwise rotation
    def rotate2(self, id1, id2, id3, id4):
         # Access the colors of the triangles with the specified IDs
        color1 = self.triangles[id1]['color']
        color2 = self.triangles[id2]['color']
        color3 = self.triangles[id3]['color']
        color4 = self.triangles[id4]['color']

        # Perform a color swap in a circular manner
        self.triangles[id1]['color'] = color2
        self.triangles[id2]['color'] = color3
        self.triangles[id3]['color'] = color4
        self.triangles[id4]['color'] = color1

        # Update the canvas to reflect the new colors
        for triangle in [id1, id2, id3, id4]:
            self.update_triangle_color(triangle)

    def update_triangle_color(self, triangle_id):
        # Update the color of the triangle with the specified ID on the canvas
        triangle = self.triangles[triangle_id]
        self.canvas.itemconfig(f"triangle_{triangle_id}", fill=triangle['color'])














# ------------------- MAIN -----------------------#
root = Tk()
root.resizable(0, 0)
app = PyraminxGui(root)
root.mainloop()
