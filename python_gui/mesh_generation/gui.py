#
# Title: gui.py
# Author: Matthew Smith 22173112
# Date: 19/03/26
# Purpose:
#   GUIManager Class:
#       Manages drawing the main tkinter frame and placement of "widgets" on screen
#
#   PlotWidget Class:
#       Visualises node placement on grid with x and y coords
#
#

##########################################################################################

# Imports
import tkinter as tk
from typing import List
from data_types import Vertex, Line, Triangle

##########################################################################################

class GUIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mesh App")
        self.root.geometry("1000x700")

        # Store components
        self.components = {}

        self.build_layout()

    # ---------- LAYOUT ----------
    def build_layout(self):
        #Plot widget
        plot = PlotWidget(self.root, width=600, height=600, scale=1.0)
        plot.place(x=50, y=50)
        self.components["plot"] = plot

        #Side panel
        panel = tk.Frame(self.root, width=250, height=600, bg="#f0f0f0")
        panel.place(x=700, y=50)
        self.components["panel"] = panel

        #Controls inside panel
        tk.Entry(panel, textvariable = plot.grid_size, font = ('calibre',10,'normal'), show = '*')
        tk.Button(panel, text="Clear", command=self.clear_plot).pack(pady=10)
        tk.Button(panel, text="Print Vertices", command=self.print_vertices).pack(pady=10)

    # ---------- BUSINESS LOGIC ----------
    def clear_plot(self):
        self.components["plot"].clear()

    def print_vertices(self):
        verts = self.components["plot"].get_vertices()
        print(verts)

    # ---------- RUN ----------
    def run(self):
        self.root.mainloop()

##########################################################################################

class PlotWidget(tk.Frame):
    def __init__(self, parent, width=500, height=500, scale=1.0, grid_size=20, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.width = width
        self.height = height
        self.scale = scale
        self.grid_size = grid_size

        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.vertices: List[Vertex] = []

        # Bind interaction
        self.canvas.bind("<Button-1>", self._on_click)

        # Initial draw
        self._draw_grid()

    # ---------- DRAWING ----------
    def _draw_grid(self):
        step = int(self.grid_size * self.scale)

        for x in range(0, self.width, step):
            self.canvas.create_line(x, 0, x, self.height, fill="#e0e0e0")

        for y in range(0, self.height, step):
            self.canvas.create_line(0, y, self.width, y, fill="#e0e0e0")

    def _draw_vertex(self, x, y):
        r = 3
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

    # ---------- INTERACTION ----------
    def _snap_to_grid(self, x, y):
        step = self.grid_size * self.scale
        return (
            round(x / step) * step,
            round(y / step) * step
        )

    def _on_click(self, event):
        x, y = self._snap_to_grid(event.x, event.y)

        v = Vertex(x, y)
        self.vertices.append(v)

        self._draw_vertex(x, y)

    # ---------- PUBLIC API ----------
    def set_grid_size(self, grid_size: float):
        self.grid_size = grid_size

    def get_vertices(self) -> List[Vertex]:
        return self.vertices

    def clear(self):
        self.canvas.delete("all")
        self.vertices.clear()
        self._draw_grid()