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
from plot_widget import PlotWidget

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