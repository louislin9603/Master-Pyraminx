import tkinter as tk
from tkinter import ttk
import random

class PyraminxSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Pyraminx Simulator")
        self.canvas = tk.Canvas(master, width=1500, height=1000)
        self.canvas.pack()

        self.colors = ["red", "blue", "green", "yellow", "black"]
        self.reset()

        self.create_buttons()
        self.create_randomize_widget()

    def reset(self):
        self.current_colors = [0]*16 + [1]*16 + [2]*16 + [3]*16
        self.update_gui()

    def create_buttons(self):
        moves = [
            ("Red Top", self.r1), ("Red Top Counter", self.r1p),
            ("Red Middle", self.r2), ("Red Middle Counter", self.r2p),
            ("Red Bottom", self.r3), ("Red Bottom Counter", self.r3p),
            ("Blue Top", self.b1), ("Blue Top Counter", self.b1p),
            ("Blue Middle", self.b2), ("Blue Middle Counter", self.b2p),
            ("Blue Bottom", self.b3), ("Blue Bottom Counter", self.b3p),
            ("Green Top", self.g1), ("Green Top Counter", self.g1p),
            ("Green Middle", self.g2), ("Green Middle Counter", self.g2p),
            ("Green Bottom", self.g3), ("Green Bottom Counter", self.g3p),
            ("Yellow Top", self.y1), ("Yellow Top Counter", self.y1p),
            ("Yellow Middle", self.y2), ("Yellow Middle Counter", self.y2p),
            ("Yellow Bottom", self.y3), ("Yellow Bottom Counter", self.y3p),
        ]

        for i, (text, command) in enumerate(moves):
            btn = tk.Button(self.master, text=text, command=command, bg=text.split()[0].lower())
            btn.place(x=1000, y=50+i*30)

    def create_randomize_widget(self):
        self.entry = tk.Entry(self.master)
        self.entry.place(x=850, y=770)
        btn = tk.Button(self.master, text="Randomize", command=self.randomize, bg='grey')
        btn.place(x=1000, y=770)

    def randomize(self):
        moves = int(self.entry.get())
        move_methods = [getattr(self, name) for name in dir(self) if name[0] in 'rbgy' and name[-1] != 'p' and len(name) == 2]
        for _ in range(moves):
            random.choice(move_methods)()

    def update_gui(self):
        self.canvas.delete("all")
        if self.is_solved():
            self.canvas.create_text(300, 50, text="SOLVED!!!", fill="black", font=('Helvetica 15 bold'))
        self.draw_face(500, 150, self.current_colors[:16], False)
        self.draw_face(500, 610, self.current_colors[16:32], True)
        self.draw_face(300, 330, self.current_colors[32:48], True)
        self.draw_face(700, 330, self.current_colors[48:], True)

    def draw_face(self, x, y, colors, inverted):
        for i, color in enumerate(colors):
            self.draw_triangle(x, y, i, color, inverted)

    def draw_triangle(self, x, y, i, color, inverted):
        row = i // 4
        col = i % 4
        tx = x + (col - row) * 30
        ty = y + row * 60
        points = self.triangle_points(tx, ty, inverted)
        self.canvas.create_polygon(points, fill=self.colors[color], outline="black")

    def triangle_points(self, x, y, inverted):
        if inverted:
            return [x, y, x-30, y-50, x+30, y-50]
        else:
            return [x, y-50, x-30, y, x+30, y]

    def is_solved(self):
        return all(all(c == color[0] for c in color) for color in [self.current_colors[i:i+16] for i in range(0, 64, 16)])

    def cycle3(self, a, b, c):
        self.current_colors[a], self.current_colors[b], self.current_colors[c] = \
        self.current_colors[c], self.current_colors[a], self.current_colors[b]

    # Red face moves
    def r1(self):
        self.cycle3(16, 63, 41)
        self.update_gui()

    def r1p(self):
        self.cycle3(16, 41, 63)
        self.update_gui()

    def r2(self):
        self.cycle3(36, 19, 61)
        self.cycle3(42, 18, 62)
        self.cycle3(43, 17, 56)
        self.update_gui()

    def r2p(self):
        self.cycle3(36, 61, 19)
        self.cycle3(42, 62, 18)
        self.cycle3(43, 56, 17)
        self.update_gui()

    def r3(self):
        self.cycle3(32, 31, 57)
        self.cycle3(34, 30, 58)
        self.cycle3(35, 29, 52)
        self.cycle3(39, 28, 53)
        self.cycle3(40, 27, 49)
        self.cycle3(46, 26, 50)
        self.cycle3(47, 25, 48)
        self.update_gui()

    def r3p(self):
        self.cycle3(32, 57, 31)
        self.cycle3(34, 58, 30)
        self.cycle3(35, 52, 29)
        self.cycle3(39, 53, 28)
        self.cycle3(40, 49, 27)
        self.cycle3(46, 50, 26)
        self.cycle3(47, 48, 25)
        self.update_gui()

    # Blue face moves
    def b1(self):
        self.cycle3(47, 0, 57)
        self.update_gui()

    def b1p(self):
        self.cycle3(47, 57, 0)
        self.update_gui()

    def b2(self):
        self.cycle3(45, 1, 52)
        self.cycle3(46, 2, 58)
        self.cycle3(40, 3, 59)
        self.update_gui()

    def b2p(self):
        self.cycle3(45, 52, 1)
        self.cycle3(46, 58, 2)
        self.cycle3(40, 59, 3)
        self.update_gui()

    def b3(self):
        self.cycle3(41, 9, 48)
        self.cycle3(42, 10, 50)
        self.cycle3(36, 11, 51)
        self.cycle3(37, 12, 55)
        self.cycle3(33, 13, 56)
        self.cycle3(34, 14, 62)
        self.cycle3(32, 15, 63)
        self.update_gui()

    def b3p(self):
        self.cycle3(41, 48, 9)
        self.cycle3(42, 50, 10)
        self.cycle3(36, 51, 11)
        self.cycle3(37, 55, 12)
        self.cycle3(33, 56, 13)
        self.cycle3(34, 62, 14)
        self.cycle3(32, 63, 15)
        self.update_gui()

    # Green face moves
    def g1(self):
        self.cycle3(48, 15, 31)
        self.update_gui()

    def g1p(self):
        self.cycle3(48, 31, 15)
        self.update_gui()

    def g2(self):
        self.cycle3(49, 13, 24)
        self.cycle3(50, 14, 30)
        self.cycle3(51, 8, 29)
        self.update_gui()

    def g2p(self):
        self.cycle3(49, 24, 13)
        self.cycle3(50, 30, 14)
        self.cycle3(51, 29, 8)
        self.update_gui()

    def g3(self):
        self.cycle3(63, 0, 25)
        self.cycle3(62, 2, 26)
        self.cycle3(61, 1, 20)
        self.cycle3(60, 5, 21)
        self.cycle3(59, 4, 17)
        self.cycle3(58, 10, 18)
        self.cycle3(57, 9, 16)
        self.update_gui()

    def g3p(self):
        self.cycle3(63, 25, 0)
        self.cycle3(62, 26, 2)
        self.cycle3(61, 20, 1)
        self.cycle3(60, 21, 5)
        self.cycle3(59, 17, 4)
        self.cycle3(58, 18, 10)
        self.cycle3(57, 16, 9)
        self.update_gui()

    # Yellow face moves
    def y1(self):
        self.cycle3(32, 25, 9)
        self.update_gui()

    def y1p(self):
        self.cycle3(32, 9, 25)
        self.update_gui()

    def y2(self):
        self.cycle3(27, 4, 33)
        self.cycle3(26, 10, 34)
        self.cycle3(20, 11, 35)
        self.update_gui()

    def y2p(self):
        self.cycle3(27, 33, 4)
        self.cycle3(26, 34, 10)
        self.cycle3(20, 35, 11)
        self.update_gui()

    def y3(self):
        self.cycle3(41, 31, 0)
        self.cycle3(42, 30, 2)
        self.cycle3(43, 24, 3)
        self.cycle3(44, 23, 7)
        self.cycle3(45, 19, 8)
        self.cycle3(46, 18, 14)
        self.cycle3(47, 16, 15)
        self.update_gui()

    def y3p(self):
        self.cycle3(41, 0, 31)
        self.cycle3(42, 2, 30)
        self.cycle3(43, 3, 24)
        self.cycle3(44, 7, 23)
        self.cycle3(45, 8, 19)
        self.cycle3(46, 14, 18)
        self.cycle3(47, 15, 16)
        self.update_gui()

if __name__ == "__main__":
    root = tk.Tk()
    app = PyraminxSimulator(root)
    root.mainloop()