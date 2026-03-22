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
import pandas as pd
from gui_components.viewport import Viewport
from gui_components.properties_window import PropertiesWindow
from data_types import ExcelOutputFormat, NodeType

##########################################################################################

class GUIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mesh App")
        self.root.geometry("1200x800")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Store components in array
        self.components = {}

        # Function to array all components nicely on screen
        self.build_layout()

    # ---------- LAYOUT ----------
    def build_layout(self):
        # Viewport
        plot = Viewport(self.root, width=800, height=600)
        plot.place(x=50, y=50)
        self.components["plot"] = plot

        # Side panel
        properties = PropertiesWindow(self.root, width=250, height=600)
        properties.place(x=900, y=50)
        self.components["properties"] = properties

        exp_button = tk.Button(self.root, text="Export to data_structure.xlsx", command=self.export_excel)
        exp_button.place(x=900, y=400)

    # ---------- BUSINESS LOGIC ----------
    def clear_plot(self):
        self.components["plot"].clear()

    def export_excel(self):
        output = self.construct_output()
        self.write_to_excel(output, filename='data_structure.xlsx')

    def construct_output(self):
        ### Get Nodes and material Properties from gui components ###
        nodes = self.components["plot"].get_nodes()
        triangles = self.components["plot"].get_triangles()
        #forces = self.components["plot"].get_forces()
        material_properties = self.components["properties"].get_material_properties()

        # Geometric representation
        n_element = len(triangles)
        n_nodes = len(nodes)
        ncon1, ncon2, ncon3 = [], [], []  # TODO: fill from elements
        X = [node.x for node in nodes]
        Y = [node.y for node in nodes] 
        F = [0.0] * (2 * n_nodes)  # placeholder
        A = 0                      # Area is handled in MATLAB -> here for poserity

        # Boundary Conditions
        NDU = sum(1 for node in nodes if node.type != NodeType.FIXED)    # NDU is the number of non-fixed nodes
        dzero = list(range(1, len(nodes) + 1))                           # dzero is an indexed list of the n_nodes

        # Material Properties
        E = material_properties["Young's Modulus"] 
        v = material_properties["Poisson's Ratio"]
        t = material_properties["Thickness"]

        # Assign variables to ExcelOutputFormat
        output = ExcelOutputFormat(
            n_element=n_element,
            n_nodes=n_nodes,
            ncon1=ncon1,
            ncon2=ncon2,
            ncon3=ncon3,
            X=X,
            Y=Y,
            E=E,
            A=0,
            F=F,
            NDU=NDU,
            dzero=dzero,
            v=v,
            t=t
        )

        return output

    def write_to_excel(self, output, filename):

        data = {
            "n_element": [output.n_element],
            "n_nodes": [output.n_nodes],
            "ncon1": [output.ncon1],
            "ncon2": [output.ncon2],
            "ncon3": [output.ncon3],
            "X": [output.X],
            "Y": [output.Y],
            "E": [output.E],
            "A": [output.A],
            "F": [output.F],
            "NDU": [output.NDU],
            "dzero": [output.dzero],
            "v": [output.v],
            "t": [output.t],
        }

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)

    # ---------- RUN ----------
    def run(self):
        self.root.mainloop()