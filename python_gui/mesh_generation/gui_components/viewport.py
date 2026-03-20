#
# Title: viewport.py
# Author: Matthew Smith 22173112
# Date: 20/03/26
# Purpose:
# - Create basic 2D viewport where user can place and delete verticies
# - Allow user to Pan X/Y and Zoom in viewport
# - 
#

import math
import tkinter as tk
from typing import List
from data_types import Node, NodeType

class Viewport(tk.Frame):

    def __init__(self, parent, width=800, height=600):
        super().__init__(parent)

        self.scale = 50.0          # pixels per world unit
        self.grid_step = 1.0       # world units
        self.x_offset = width / 2  # center origin
        self.y_offset = height / 2

        self.node_type = NodeType.NORMAL
        self.nodes: List[Node] = []

        self._drag_start = None

        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # bindings
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Double-Button-1>", self._on_double_left_click)
        self.canvas.bind("<ButtonPress-3>", self._on_drag_start)
        self.canvas.bind("<B3-Motion>", self._on_drag_motion)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Configure>", lambda e: self._redraw())

        self.bind_all("1", lambda e: self._set_type(NodeType.NORMAL))
        self.bind_all("2", lambda e: self._set_type(NodeType.FIXED))
        self.bind_all("3", lambda e: self._set_type(NodeType.FORCE))

        self._redraw()
    
    ############################################################################
    # ---------- TRANSFORMS ----------
    ############################################################################

    def world_to_screen(self, x, y):
        return x * self.scale + self.x_offset, y * self.scale + self.y_offset

    def screen_to_world(self, px, py):
        return (px - self.x_offset) / self.scale, (py - self.y_offset) / self.scale

    def snap(self, px, py):
        x, y = self.screen_to_world(px, py)
        gx = round(x / self.grid_step) * self.grid_step
        gy = round(y / self.grid_step) * self.grid_step
        return gx, gy

    ############################################################################
    # ---------- DRAWING ----------
    ############################################################################

    def _draw_grid(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        x0, y0 = self.screen_to_world(0, 0)
        x1, y1 = self.screen_to_world(w, h)

        step = self.grid_step

        for x in self._frange(math.floor(x0), math.ceil(x1), step):
            px, _ = self.world_to_screen(x, 0)
            self.canvas.create_line(px, 0, px, h, fill="#e0e0e0")

        for y in self._frange(math.floor(y0), math.ceil(y1), step):
            _, py = self.world_to_screen(0, y)
            self.canvas.create_line(0, py, w, py, fill="#e0e0e0")

        # axes
        px0, _ = self.world_to_screen(0, 0)
        _, py0 = self.world_to_screen(0, 0)
        self.canvas.create_line(px0, 0, px0, h, fill="black", width=2)
        self.canvas.create_line(0, py0, w, py0, fill="black", width=2)

    def _draw_nodes(self):
        r = self.scale / 6
        for node in self.nodes:
            px, py = self.world_to_screen(node.x, node.y)
            
            if node.type == NodeType.NORMAL:
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="black",width=2)
            elif node.type == NodeType.FIXED:
                self.canvas.create_oval(px-r, py-r, px+r, py+r, fill="black")
            elif node.type == NodeType.FORCE:
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="red", width=2)

    def _draw_tooltip(self, px, py, node):
        self.canvas.delete("tooltip")

        text = f"x={node.x}, y={node.y}\n{node.type.name}"

        text_id = self.canvas.create_text(
            px + 10, py - 10,
            text=text,
            anchor="sw",
            tags="tooltip"
        )

        bbox = self.canvas.bbox(text_id)
        if bbox:
            self.canvas.create_rectangle(
                bbox[0]-3, bbox[1]-3,
                bbox[2]+3, bbox[3]+3,
                fill="lightyellow",
                outline="gray",
                tags="tooltip"
            )
            self.canvas.tag_raise(text_id)

    def _redraw(self):
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_nodes()

    ############################################################################
    # ---------- CONTROLS ----------
    ############################################################################

    def _on_left_click(self, event):
        x, y = self.snap(event.x, event.y)
        if not any(n.x == x and n.y == y for n in self.nodes):
            self.nodes.append(Node(x, y, self.node_type))
            self._redraw()

    def _on_double_left_click(self, event):
        x, y = self.snap(event.x, event.y)
        self.nodes = [n for n in self.nodes if not (n.x == x and n.y == y)]
        self._redraw()

    def _on_mouse_move(self, event):
        node = self._find_nearest_node(event.x, event.y)

        if node: self._draw_tooltip(event.x, event.y, node)
        else: self.canvas.delete("tooltip")

    def _on_drag_start(self, event):
        self._drag_start = (event.x, event.y)

    def _on_drag_motion(self, event):
        dx = event.x - self._drag_start[0]
        dy = event.y - self._drag_start[1]

        self.x_offset += dx
        self.y_offset += dy

        self._drag_start = (event.x, event.y)
        self._redraw()

    def _on_mouse_wheel(self, event):
        factor = 1.1 if event.delta > 0 else 0.9

        # zoom at cursor
        self.x_offset = event.x - factor * (event.x - self.x_offset)
        self.y_offset = event.y - factor * (event.y - self.y_offset)

        self.scale *= factor
        self._redraw()

    def _set_type(self, t):
        self.node_type = t

    ############################################################################
    # ---------- UTILITY FUNCTIONS ----------
    ############################################################################

    # float range
    def _frange(self, start, stop, step):
        x = start
        while x <= stop:
            yield x
            x += step

    def _find_nearest_node(self, px, py):
        x, y = self.screen_to_world(px, py)
        radius = 0.2  # world units

        for node in self.nodes:
            dx = node.x - x
            dy = node.y - y
            if dx*dx + dy*dy <= radius * radius:
                return node
        return None
    
    ############################################################################
    # ---------- PUBLIC API ----------
    ############################################################################

    def get_nodes(self):
        return list(self.nodes)

    def clear(self):
        self.nodes.clear()
        self._redraw()