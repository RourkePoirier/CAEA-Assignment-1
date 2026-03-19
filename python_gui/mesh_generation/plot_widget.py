import tkinter as tk
from typing import List
from data_types import Vertex, VertexType
import math

class PlotWidget(tk.Frame):
    def __init__(self, parent, width=500, height=500, scale=1.0, grid_size=20.0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.scale = scale
        self.x_offset = 0
        self.y_offset = 0
        self.grid_size = grid_size
        self.vertex_type = VertexType.NORMAL
        self.vertices: List[Vertex] = []

        self._drag_start = None
        self._tooltip = None

        # Canvas setup
        self.canvas = tk.Canvas(self, width=width, height=height, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Bind interactions
        self.canvas.bind("<Button-1>", self._on_left_click)
        self.canvas.bind("<Button-3>", self._on_right_click)
        self.canvas.bind("<ButtonPress-2>", self._on_drag_start)
        self.canvas.bind("<B2-Motion>", self._on_drag_motion)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Configure>", lambda e: self._redraw())

        # Keybinds for vertex types
        self.bind_all("1", lambda e: self.set_vertex_type(VertexType.NORMAL))
        self.bind_all("2", lambda e: self.set_vertex_type(VertexType.FIXED))
        self.bind_all("3", lambda e: self.set_vertex_type(VertexType.FORCE))

        self._redraw()

    # ---------- DRAW ----------
    def _draw_grid(self):
        step = self.grid_size * self.scale
        if step <= 0:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        first_gx = math.ceil(-self.x_offset / step)
        first_gy = math.ceil(-self.y_offset / step)

        gx = first_gx
        while True:
            px = gx * step + self.x_offset
            if px > w:
                break
            color = "black" if gx == 0 else "#e0e0e0"
            width = 2 if gx == 0 else 1
            self.canvas.create_line(px, 0, px, h, fill=color, width=width)
            gx += 1

        gy = first_gy
        while True:
            py = gy * step + self.y_offset
            if py > h:
                break
            color = "black" if gy == 0 else "#e0e0e0"
            width = 2 if gy == 0 else 1
            self.canvas.create_line(0, py, w, py, fill=color, width=width)
            gy += 1

    def _draw_vertex(self, v: Vertex):
        gx = v.x * self.grid_size * self.scale + self.x_offset
        gy = v.y * self.grid_size * self.scale + self.y_offset
        r = self.grid_size * self.scale / 4

        if v.type == VertexType.NORMAL:
            self.canvas.create_oval(gx - r, gy - r, gx + r, gy + r, outline="black", width=2)
        elif v.type == VertexType.FIXED:
            self.canvas.create_oval(gx - r, gy - r, gx + r, gy + r, fill="black")
        elif v.type == VertexType.FORCE:
            self.canvas.create_oval(gx - r, gy - r, gx + r, gy + r, outline="red", width=2)

    def _redraw(self):
        self.canvas.delete("all")
        self._draw_grid()
        for v in self.vertices:
            self._draw_vertex(v)

    # ---------- COORDINATE CONVERSION ----------
    def _snap_to_grid(self, x_pixel, y_pixel):
        gx_unit = round((x_pixel - self.x_offset) / (self.grid_size * self.scale))
        gy_unit = round((y_pixel - self.y_offset) / (self.grid_size * self.scale))
        return gx_unit, gy_unit

    # ---------- INTERACTION ----------
    def _on_left_click(self, event):
        gx_unit, gy_unit = self._snap_to_grid(event.x, event.y)
        for v in self.vertices:
            if v.x == gx_unit and v.y == gy_unit:
                return
        self.vertices.append(Vertex(gx_unit, gy_unit, self.vertex_type))
        self._redraw()

    def _on_right_click(self, event):
        gx_unit, gy_unit = self._snap_to_grid(event.x, event.y)
        idx = self._find_nearest_vertex(gx_unit, gy_unit)
        if idx is not None:
            del self.vertices[idx]
            self._redraw()

    # ---------- SELECTION ----------
    def _find_nearest_vertex(self, gx_unit, gy_unit):
        radius = 0.5
        r2 = radius * radius
        for i, v in enumerate(self.vertices):
            dx = v.x - gx_unit
            dy = v.y - gy_unit
            if dx * dx + dy * dy <= r2:
                return i
        return None

    # ---------- TOOLTIP ----------
    def _on_mouse_move(self, event):
        gx_unit, gy_unit = self._snap_to_grid(event.x, event.y)
        idx = self._find_nearest_vertex(gx_unit, gy_unit)
        if idx is not None:
            v = self.vertices[idx]
            self._show_tooltip(event.x, event.y, f"x={v.x}, y={v.y}\ntype={v.type.name}")
        else:
            self._hide_tooltip()

    def _show_tooltip(self, x, y, text):
        self._hide_tooltip()
        # Draw text first to measure it
        self._tooltip_text = self.canvas.create_text(
            x + 12, y - 12,
            text=text,
            anchor="sw",
            font=("TkDefaultFont", 9),
            fill="black",
            tags="tooltip"
        )
        bbox = self.canvas.bbox(self._tooltip_text)
        if bbox:
            pad = 3
            self._tooltip_bg = self.canvas.create_rectangle(
                bbox[0] - pad, bbox[1] - pad,
                bbox[2] + pad, bbox[3] + pad,
                fill="lightyellow", outline="gray",
                tags="tooltip"
            )
            # Raise text above background rect
            self.canvas.tag_raise(self._tooltip_text)

    def _hide_tooltip(self):
        self.canvas.delete("tooltip")
        self._tooltip = None

    # ---------- PANNING ----------
    def _on_drag_start(self, event):
        self._drag_start = (event.x, event.y)

    def _on_drag_motion(self, event):
        if self._drag_start:
            dx = event.x - self._drag_start[0]
            dy = event.y - self._drag_start[1]
            self.x_offset += dx
            self.y_offset += dy
            self._drag_start = (event.x, event.y)
            self._redraw()

    # ---------- ZOOM ----------
    def _on_mouse_wheel(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        mouse_x = event.x
        mouse_y = event.y

        self.x_offset = mouse_x - factor * (mouse_x - self.x_offset)
        self.y_offset = mouse_y - factor * (mouse_y - self.y_offset)

        self.scale *= factor
        self._redraw()

    # ---------- API ----------
    def get_vertices(self) -> List[Vertex]:
        return list(self.vertices)

    def add_vertices(self, new_vertices: List[Vertex]):
        for v in new_vertices:
            if not any(ev.x == v.x and ev.y == v.y for ev in self.vertices):
                self.vertices.append(v)
        self._redraw()

    def set_vertex_type(self, vt: VertexType):
        self.vertex_type = vt

    def clear(self):
        self.vertices.clear()
        self._redraw()

    def set_scale(self, scale: float):
        if scale > 0:
            self.scale = scale
            self._redraw()

    def set_x_offset(self, x_offset: float):
        self.x_offset = x_offset
        self._redraw()

    def set_y_offset(self, y_offset: float):
        self.y_offset = y_offset
        self._redraw()