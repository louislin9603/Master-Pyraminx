from tkinter import *
import random

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
    def __init__(self, root):
        self.root = root
        self.pyraminx = Pyraminx()
        self.triangles = []

        root.title("Pyraminx Puzzle")

        self.canvas = Canvas(root, width=800, height=800, bg='white')
        self.canvas.pack()

        self.button = Button(root, text="Randomize", command=self.on_button_click)
        self.button.pack()

        self.updateGui()

    def updateGui(self):
        self.canvas.delete("all")
        self.triangles = []
        faces = self.pyraminx.faces

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
        for i in range(4):
            for j in range(i+1):
                # Draw triangles in rows
                self.draw_triangle(x + (j * 40) - (i * 20), y + (i * 40), face[i][j])
                self.canvas.create_text(x + (j * 40) - (i * 20), y + (i * 40), text=f"{i},{j}", fill="black", font=('Arial', 8))    
                if j != i:  # Skip drawing upside-down triangle at the end of each row
                    self.draw_upsidedown_triangle(x + (j * 40) - (i * 20) + size, y + (i * 40), face[i][j])
                    self.canvas.create_text(x + (j * 40) - (i * 20) + size, y + (i * 40), text=f"{i},{j}", fill="black", font=('Arial', 8))


    def draw_triangle(self, x, y, color, size=20):
        x1, x2, x3 = x, x - size, x + size
        y1, y2, y3 = y - size, y + size, y + size
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black')

    def draw_upsidedown_triangle(self, x, y, color, size=20):
        x1, x2, x3 = x, x - size, x + size
        y1, y2, y3 = y + size, y - size, y - size
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black')

    def on_button_click(self):
        self.pyraminx.randomize()
        self.updateGui()

# ------------------- MAIN -----------------------#
root = Tk()
root.resizable(0, 0)
app = PyraminxGui(root)
root.mainloop()
