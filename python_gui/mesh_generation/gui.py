#
# Title: gui.py
# Author: Matthew Smith 22173112
# Date: 19/03/26
# Purpose:
#    Manages drawing the main tkinter frame and placement of "widgets" on screen
#

##########################################################################################

# Imports
import tkinter as tk
from gui_components.viewport import Viewport
from gui_components.properties_window import PropertiesWindow

##########################################################################################

class GUIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mesh App")
        self.root.geometry("1200x800")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Store components
        self.components = {}

        self.build_layout()

    # ---------- LAYOUT ----------
    def build_layout(self):
        # Viewport
        plot = Viewport(self.root, width=800, height=600)
        plot.place(x=50, y=50)
        self.components["plot"] = plot

        # Side panel
        panel = PropertiesWindow(self.root, width=250, height=600)
        panel.place(x=900, y=50)
        self.components["panel"] = panel


    # ---------- BUSINESS LOGIC ----------
    def clear_plot(self):
        self.components["plot"].clear()

    def save(self):
        verts = self.components["plot"].get_nodes()
        print(verts)

    # ---------- RUN ----------
    def run(self):
        self.root.mainloop()