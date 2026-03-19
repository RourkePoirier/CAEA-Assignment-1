
import tkinter as tk
from data_types import Vertex, ForceVector
from typing import List

class MeshGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2D Mesh Generator")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.vertices: List[Vertex] = []
        self.forces: List[ForceVector] = []

        self.canvas.bind("<Button-1>", self.add_vertex)

    def add_vertex(self, event):
        v = Vertex(event.x, event.y)
        self.vertices.append(v)
        self.canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black")
        print(f"Added vertex: {v}")

    def run(self):
        self.root.mainloop()