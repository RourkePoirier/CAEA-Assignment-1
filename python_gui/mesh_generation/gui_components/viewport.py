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
import tkinter.simpledialog as sd
from typing import List
from data_types import Node, Tool, NodeType, Triangle, Force
from gui_components.mesh_generator import generate_triangular_mesh
from gui_components.force_dialog import ForceDialog

class Viewport(tk.Frame):

    def __init__(self, parent, width=800, height=600):
        super().__init__(parent)

        self.scale = 50.0          # pixels per world unit
        self.grid_step = 1.0       # world units
        self.x_offset = width / 2  # center origin
        self.y_offset = height / 2

        # Nodes and Triangles
        self.nodes:     List[Node] = []
        self.triangles: List[Triangle] = []
        self.forces:    List[Force] = []

        self.tool = Tool.NODE # Default tool is node tool
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

        self.bind_all("1", lambda e: self._set_tool(Tool.NODE))
        self.bind_all("2", lambda e: self._set_tool(Tool.FIXED_NODE))
        self.bind_all("3", lambda e: self._set_tool(Tool.FORCE))

        self._redraw()
    
    ############################################################################
    # ---------- TRANSFORMS ----------
    ############################################################################
    
    # Ensure Y is flipped (y in Tkinter is negative)
    def world_to_screen(self, x, y):
        return x * self.scale + self.x_offset, -y * self.scale + self.y_offset

    def screen_to_world(self, px, py):
        return (px - self.x_offset) / self.scale, -(py - self.y_offset) / self.scale

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
                self.canvas.create_oval(px-r, py-r, px+r, py+r, outline="red",width=2)

    def _draw_forces(self):

        arrow_scale = 0.2  # scaling factor for visualization

        for f in self.forces:
            # starting point (node position)
            x0, y0 = self.world_to_screen(f.node.x, f.node.y)

            # compute vector end point
            rad = math.radians(f.angle)
            dx = f.magnitude * math.cos(rad) * arrow_scale
            dy = f.magnitude * math.sin(rad) * arrow_scale

            # flip dy for screen coordinates
            x1, y1 = self.world_to_screen(f.node.x + dx, f.node.y + dy)

            # draw arrow
            self.canvas.create_line(
                x0, y0, x1, y1,
                arrow=tk.LAST,
                fill="blue",
                width=2
            )

    def _draw_triangles(self):

        self.triangles = generate_triangular_mesh(self.nodes)

        for tri in self.triangles:
            n1, n2, n3 = tri.Nodes

            p1 = self.world_to_screen(n1.x, n1.y)
            p2 = self.world_to_screen(n2.x, n2.y)
            p3 = self.world_to_screen(n3.x, n3.y)

            # Draw triangle edges
            self.canvas.create_line(*p1, *p2, fill="red")
            self.canvas.create_line(*p2, *p3, fill="red")
            self.canvas.create_line(*p3, *p1, fill="red")

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
        self._draw_triangles() 
        self._draw_forces()
        self._draw_nodes()

    ############################################################################
    # ---------- CONTROLS ----------
    ############################################################################

    def _on_left_click(self, event):

        # Snap to nearest grid point
        x, y = self.snap(event.x, event.y)

        # if there are no nodes at point
        if not self._node_exists_at(x, y):
            
            # Insert Node based on currently selected Tool
            match(self.tool):

                case Tool.NODE:
                    self.nodes.append(Node(x, y, NodeType.NORMAL))

                case Tool.FIXED_NODE:
                    self.nodes.append(Node(x, y, NodeType.FIXED))

                case Tool.FORCE:
                    dlg = ForceDialog(self, "Define Force")
                    if dlg.magnitude is None or dlg.angle is None: return  # user cancelled

                    node = Node(x, y, NodeType.FORCE)
                    self.nodes.append(node)
                    self.forces.append(Force(node, magnitude=dlg.magnitude, angle=dlg.angle))
                                    
                
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

    def _set_tool(self, t):
        self.tool = t

    ############################################################################
    # ---------- UTILITY FUNCTIONS ----------
    ############################################################################

    # float range function (+ive and -ive)
    def _frange(self, start, stop, step):
        if step == 0:
            return
        x = start
        if start < stop:
            while x <= stop:
                yield x
                x += step
        else:
            while x >= stop:
                yield x
                x -= step

    def _find_nearest_node(self, px, py):
        x, y = self.screen_to_world(px, py)
        radius = 0.2  # world units

        for node in self.nodes:
            dx = node.x - x
            dy = node.y - y
            if dx*dx + dy*dy <= radius * radius:
                return node
        return None
    
    # Node coord collision test
    def _node_exists_at(self, x, y) -> bool:
        return any(n.x == x and n.y == y for n in self.nodes)
    
    ############################################################################
    # ---------- PUBLIC API ----------
    ############################################################################

    def get_nodes(self):
        return list(self.nodes)

    def get_triangles(self):
        return list(self.triangles)
    
    def clear(self):
        self.nodes.clear()
        self._redraw()