# mesh_generator.py
#
# Hi Rourke - extend this to implement whatever triangulation logic :)
# Currently there is a dalanuay implementation I am wrapping from scipy library
# So long as you follow the function signature (input: List of Nodes | Output List of Triangles)
# Then any algorithm can be implemented here and it should show up nicely :)

from typing import List
from scipy.spatial import Delaunay
import numpy as np

from data_types import Node, Triangle

def generate_triangular_mesh(nodes: List[Node]) -> List[Triangle]:

    # No triangles if there are less than 3 nodes xD
    if len(nodes) < 3: return []

    # Convert to numpy points
    points = np.array([[node.x, node.y] for node in nodes])

    tri = Delaunay(points)

    triangles: List[Triangle] = []

    for simplex in tri.simplices:
        n1 = nodes[simplex[0]]
        n2 = nodes[simplex[1]]
        n3 = nodes[simplex[2]]

        # Ensure consistent CCW orientation (important for FEA later)
        if not is_ccw(n1, n2, n3):
            n2, n3 = n3, n2

        triangles.append(Triangle(Nodes=(n1, n2, n3)))

    return triangles


def is_ccw(n1: Node, n2: Node, n3: Node) -> bool:
    return (n2.x - n1.x)*(n3.y - n1.y) - (n2.y - n1.y)*(n3.x - n1.x) > 0