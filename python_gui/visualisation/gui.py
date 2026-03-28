##########################################################################################

# Imports
import pandas as pd
import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


##########################################################################################

class GUIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Visualisation")
        self.root.geometry("1200x800")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # - Read data_structure -

        # Prob should not make this hard coded
        data_structure = pd.read_excel('data_structure.xlsx')

        n_element=data_structure["n_element"][0]
        n_nodes=data_structure["n_nodes"][0]
        ncon1=data_structure["ncon1"].dropna().to_numpy()
        ncon2=data_structure["ncon2"].dropna().to_numpy()
        ncon3=data_structure["ncon3"].dropna().to_numpy()
        X=data_structure["X"].dropna().to_numpy()
        Y=data_structure["Y"].dropna().to_numpy()
        E=data_structure["E"][0]
        A=data_structure["A"][0]
        F=data_structure["F"].dropna().to_numpy()
        NDU=data_structure["NDU"][0]
        dzero=data_structure["dzero"].dropna().to_numpy()
        v=data_structure["v"][0]
        t=data_structure["t"][0]
        

        # The following is the post_processing matlab function
        # TODO 

        # - matplot -
        figure = Figure(figsize=(5, 4), dpi=100)

        ax = figure.add_subplot(111)
        t = np.arange(0, 3, .01)
        ax.plot(t, 2 * np.sin(2 * np.pi * t))

        # - Draw matplot in tkinter -
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # ---------- LAYOUT ----------
    def build_layout(self):
        return []

# ---------- RUN ----------
    def run(self):
        self.root.mainloop()
