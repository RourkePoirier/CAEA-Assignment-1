##########################################################################################

# Imports
import pandas as pd
import tkinter as tk
from tkinter import ttk
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
        data   = pd.read_excel('data_structure.xlsx', header=None, skiprows=1).values
        U      = pd.read_excel('displacement.xlsx',   header=None).values.flatten()
        Sx     = pd.read_excel('stress_x.xlsx',       header=None).values.flatten()
        Sy     = pd.read_excel('stress_y.xlsx',       header=None).values.flatten()
        Sxy    = pd.read_excel('stress_xy.xlsx',      header=None).values.flatten()

        # Parse structure parameters (matching MATLAB hardcoded positions)
        n_element = int(data[0, 0])
        n_nodes   = int(data[0, 1])

        # Only take first n_element rows for connectivity
        ncon = data[:n_element, 2:5].astype(int) - 1  # 0-indexed

        # Only take rows with valid X/Y data (first n_nodes rows that aren't NaN)
        xy = data[:, 5:7]
        valid = ~np.isnan(xy[:, 0])
        X = xy[valid, 0]
        Y = xy[valid, 1]

        # Trim to exactly n_nodes
        X = X[:n_nodes]
        Y = Y[:n_nodes]

        # Von Mises stress
        VM = np.sqrt(Sx**2 - Sx*Sy + Sy**2 + 3*Sxy**2)

        # Notebook with two tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=1)

        #
        #   Page 1 - Displacement
        #

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text='Deformation')
        notebook.add(tab2, text='Von Mises Stress')

        fig1 = Figure()
        ax1  = fig1.add_subplot(111)

        mesh_size = max(X.max() - X.min(), Y.max() - Y.min())
        scale = 0.1 * mesh_size / np.max(np.abs(U))

        for i in range(n_element):
            n1, n2, n3 = ncon[i]

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
            ax1.plot(x_orig, y_orig, color='blue',  linewidth=1,   label='Original'  if i == 0 else "")
            ax1.plot(x_def,  y_def,  color='red',   linewidth=2,   label='Deformed'  if i == 0 else "")

        ax1.set_aspect('equal')
        ax1.legend()
        ax1.set_title('FEA Structure: Original vs Deformed')
        ax1.axis('off')

        canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        #
        #   Page 2 - Stress
        #

        fig2 = Figure()
        ax2  = fig2.add_subplot(111)

        # tripcolor needs node-based values, so average element stresses to nodes
        node_stress     = np.zeros(len(X))
        node_stress_count = np.zeros(len(X))

        for i in range(n_element):
            n1, n2, n3 = ncon[i]
            node_stress[n1] += VM[i]
            node_stress[n2] += VM[i]
            node_stress[n3] += VM[i]
            node_stress_count[n1] += 1
            node_stress_count[n2] += 1
            node_stress_count[n3] += 1

        node_stress /= node_stress_count

        # Build triangle array for tripcolor
        triangles = ncon[:n_element]  # shape (n_element, 3)

        plot = ax2.tripcolor(X, Y, triangles, node_stress, cmap='jet', shading='gouraud')
        ax2.triplot(X, Y, triangles, color='k', linewidth=0.3, alpha=0.3)  # optional mesh overlay

        fig2.colorbar(plot, ax=ax2, label='Von Mises Stress (Pa)')
        ax2.set_aspect('equal')
        ax2.set_title('Von Mises Stress')
        ax2.axis('off')

        canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    def on_close(self):
        plt.close('all')
        self.root.quit()
        self.root.destroy()

# ---------- RUN ----------
    def run(self):
        self.root.mainloop()
