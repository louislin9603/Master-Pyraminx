from tkinter import *
from tkinter import ttk
import math
import random

class Pyraminx:
    def __init__(self):

        #Initialize faces with default colors
        self.faces = {
            'A': [["red"]*4 for _ in range(4)],
            'B': [["green"]*4 for _ in range(4)],
            'C': [["blue"]*4 for _ in range(4)],
            'D': [["yellow"]*4 for _ in range(4)],
        }

        def randomize(self):

            # Randomize each face by shuffling the colors in the 4x4 grid


class PyraminxGui:
    def __init__(self, root):
        self.root = root
        self.pyraminx = Pyraminx()

        root.title("Pyraminx Puzzle")

        self.canvas = Canvas(root, width=800, height=800, bg='white')
        self.canvas.pack()

        self.button = Button(root, text="Randomize", command=on_button_click)
        self.button.pack()

        updateGui()

        def updateGui():
            ## RED (middle)
            # Row 1
            self.draw_triangle(320,60, "red")
            # Row 2
            self.draw_triangle(300,100,"red")
            self.draw_upsidedown_triangle(320,100,"red")
            self.draw_triangle(340,100,"red")
            # Row 3
            self.draw_triangle(280,140,"red")
            self.draw_upsidedown_triangle(300,140,"red")
            self.draw_triangle(320,140,"red")
            self.draw_upsidedown_triangle(340,140,"red")
            self.draw_triangle(360,140,"red")
            # Row 4
            self.draw_triangle(260,180,"red")
            self.draw_upsidedown_triangle(280,180,"red")
            self.draw_triangle(300,180,"red")
            self.draw_upsidedown_triangle(320,180,"red")
            self.draw_triangle(340,180,"red") 
            self.draw_upsidedown_triangle(360,180,"red")
            self.draw_triangle(380,180,"red") 


            ## GREEN (left)
            # Row 1
            self.draw_upsidedown_triangle(100,60,"green")
            self.draw_triangle(120,60,"green")
            self.draw_upsidedown_triangle(140,60,"green")
            self.draw_triangle(160,60,"green")
            self.draw_upsidedown_triangle(180,60,"green")
            self.draw_triangle(200,60,"green") 
            self.draw_upsidedown_triangle(220,60,"green")
            # Row 2
            self.draw_upsidedown_triangle(120,100,"green")
            self.draw_triangle(140,100,"green")
            self.draw_upsidedown_triangle(160,100,"green")
            self.draw_triangle(180,100,"green")
            self.draw_upsidedown_triangle(200,100,"green")
            # Row 3
            self.draw_upsidedown_triangle(140,140,"green")
            self.draw_triangle(160,140,"green")
            self.draw_upsidedown_triangle(180,140,"green")
            # Row 4
            self.draw_upsidedown_triangle(160,180,"green")


            ## YELLOW (right)
            # Row 1
            self.draw_upsidedown_triangle(420,60,"yellow")
            self.draw_triangle(440,60,"yellow")
            self.draw_upsidedown_triangle(460,60,"yellow")
            self.draw_triangle(480,60,"yellow")
            self.draw_upsidedown_triangle(500,60,"yellow")
            self.draw_triangle(520,60,"yellow") 
            self.draw_upsidedown_triangle(540,60,"yellow")
            # Row 2
            self.draw_upsidedown_triangle(440,100,"yellow")
            self.draw_triangle(460,100,"yellow")
            self.draw_upsidedown_triangle(480,100,"yellow")
            self.draw_triangle(500,100,"yellow")
            self.draw_upsidedown_triangle(520,100,"yellow")
            # Row 3
            self.draw_upsidedown_triangle(460,140,"yellow")
            self.draw_triangle(480,140,"yellow")
            self.draw_upsidedown_triangle(500,140,"yellow")
            # Row 4
            self.draw_upsidedown_triangle(480,180,"yellow")


            ## BLUE (bottom)
            # Row 1
            self.draw_upsidedown_triangle(260,280,"blue")
            self.draw_triangle(280,280,"blue")
            self.draw_upsidedown_triangle(300,280,"blue")
            self.draw_triangle(320,280,"blue")
            self.draw_upsidedown_triangle(340,280,"blue")
            self.draw_triangle(360,280,"blue") 
            self.draw_upsidedown_triangle(380,280,"blue")
            # Row 2
            self.draw_upsidedown_triangle(280,320,"blue")
            self.draw_triangle(300,320,"blue")
            self.draw_upsidedown_triangle(320,320,"blue")
            self.draw_triangle(340,320,"blue")
            self.draw_upsidedown_triangle(360,320,"blue")
            # Row 3
            self.draw_upsidedown_triangle(300,360,"blue")
            self.draw_triangle(320,360,"blue")
            self.draw_upsidedown_triangle(340,360,"blue")
            # Row 4
            self.draw_upsidedown_triangle(320,400,"blue")



    def draw_triangle(self,x,y,color):

        size = 20
        x1 = x
        x2 = x - size
        x3 = x + size

        y1 = y - size
        y2 = y + size
        y3 = y + size

        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black')

    def draw_upsidedown_triangle(self, x, y,color):
        
        size = 20
        x1 = x
        x2 = x - size
        x3 = x + size

        y1 = y + size
        y2 = y - size
        y3 = y - size

        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline='black')


def on_button_click():
    print("Button was clicked")

#------------------- MAIN -----------------------#

#Create window
root = Tk()
root.resizable(0,0)
app = PyraminxGui(root)

root.mainloop()
