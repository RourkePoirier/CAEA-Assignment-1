# mesh_generator.py
#
# Hi Rourke - extend this to implement whatever triangulation logic :)
# Currently there is a dalanuay implementation I am wrapping from scipy library
# So long as you follow the function signature (input: List of Nodes | Output List of Triangles)
# Then any algorithm can be implemented here and it should show up nicely :)

from typing import List
from scipy.spatial import Delaunay
import numpy as np
import tkinter as tk

from data_types import Node, Triangle, MeshScheme

def generate_triangular_mesh(nodes: List[Node], mesh_method: tk.StringVar) -> List[Triangle]:

    # No triangles if there are less than 3 nodes xD
    if len(nodes) < 3: return []

    value = mesh_method.get()
    
    match mesh_method.get():
        case MeshScheme.DELAUNAY.value: return _delaunay(nodes)
        case MeshScheme.NOTHING.value: return _nothing(nodes)
        case _:
            print(f"Unknown mesh scheme: {mesh_method.get()}, falling back to Delaunay")
            return _delaunay(nodes)

# -- Algorithms --
def _delaunay(nodes: List[Node]) -> List[Triangle]:
    if len(nodes) < 3:
        return []

    # Convert nodes to numpy array
    points = np.array([[n.x, n.y] for n in nodes])
    tri = Delaunay(points)

    triangles: List[Triangle] = []

    for simplex in tri.simplices:
        i0, i1, i2 = simplex  # indices into nodes list
        n0, n1, n2 = nodes[i0], nodes[i1], nodes[i2]

        # Ensure CCW orientation
        if not _is_ccw(n0, n1, n2):
            i1, i2 = i2, i1  # swap indices, not Node objects
        
        triangles.append(Triangle(node_ids=(i0, i1, i2)))

    return triangles

def _nothing(nodes: List[Node]) -> List[Triangle]:
    return []

# -- Helper Methods --

def _is_ccw(n1: Node, n2: Node, n3: Node) -> bool:
    return (n2.x - n1.x)*(n3.y - n1.y) - (n2.y - n1.y)*(n3.x - n1.x) > 0
