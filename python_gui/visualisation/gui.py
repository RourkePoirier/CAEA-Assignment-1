##########################################################################################

# Imports
import pandas as pd
import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

##########################################################################################

class GUIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Visualisation")
        self.root.geometry("1200x800")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # handle close button

        # Read data
        data = pd.read_excel('data_structure.xlsx', header=None, skiprows=1).values
        U_data = pd.read_excel('displacement.xlsx', header=None).values.flatten()

        # Parse structure parameters (matching MATLAB hardcoded positions)
        n_element = int(data[0, 0])
        n_nodes   = int(data[0, 1])

        ncon = data[:, 2:5].astype(int)  # Node connectivity (1-indexed)
        X    = data[:, 5]
        Y    = data[:, 6]
        U    = U_data

        fig, ax = plt.subplots()

        scale = 1000

        for i in range(n_element):
            n1, n2, n3 = ncon[i] - 1  # Convert to 0-indexed

            # Original coordinates
            x_orig = [X[n1], X[n2], X[n3], X[n1]]
            y_orig = [Y[n1], Y[n2], Y[n3], Y[n1]]

            # Displacements (interleaved: u1,v1,u2,v2,...)
            u1, v1 = U[2*n1],   U[2*n1+1]
            u2, v2 = U[2*n2],   U[2*n2+1]
            u3, v3 = U[2*n3],   U[2*n3+1]

            # Deformed coordinates
            x_def = [X[n1] + scale*u1, X[n2] + scale*u2, X[n3] + scale*u3, X[n1] + scale*u1]
            y_def = [Y[n1] + scale*v1, Y[n2] + scale*v2, Y[n3] + scale*v3, Y[n1] + scale*v1]

            # Plot original (blue) and deformed (red)
            ax.plot(x_orig, y_orig, color='blue',  linewidth=1,   label='Original'  if i == 0 else "")
            ax.plot(x_def,  y_def,  color='red',   linewidth=2,   label='Deformed'  if i == 0 else "")

        ax.set_aspect('equal')
        ax.legend()
        ax.set_title('FEA Structure: Original vs Deformed')
        ax.axis('off')

        # The following is the post_processing matlab function
        # TODO 

        # - Draw matplot in tkinter -
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def on_close(self):
        plt.close('all')
        self.root.quit()
        self.root.destroy()

# ---------- RUN ----------
    def run(self):
        self.root.mainloop()
