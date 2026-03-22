from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum

class NodeType(Enum):
    NORMAL = 1
    FIXED = 2
    FORCE = 3

@dataclass
class Node:
    x: float
    y: float
    type: NodeType

@dataclass
class Line:
    start: Node
    end: Node

@dataclass
class Triangle:
    Nodes: Tuple[Node, Node, Node]

@dataclass
class ForceVector:
    node: Node
    angle_deg: float
    magnitude: float

# data_structure.xlsx structure made by Sarat
@dataclass
class ExcelOutputFormat:
    n_element:  int             # Number of Triangular Elements
    n_nodes:    int             # Number of Nodes
    ncon1:      List[int]       # Nodal Connectivity Matrix Column 1
    ncon2:      List[int]       # Nodal Connectivity Matrix Column 2
    ncon3:      List[int]       # Nodal Connectivity Matrix Column 3
    X:          List[float]     # Node X Coords
    Y:          List[float]     # Node Y Coords
    E:          float           # Young's Modulus
    A:          int             # Area -> purposeless (calculated in MATLAB)
    F:          List[float]     # Force Array, Tuples of force, [1000, 0] represents a 1000N Force in the x direction
    NDU:        int             # Nodal Degrees of Freedom Unconstrained (Number of non-fixed Nodes)
    dzero:      List[int]       # Increment for number of Nodes (if n=4 -> 1,2,3,4) Again purposeless, but I don't make the rules :/
    v:          float           # Poission's Ratio
    t:          float           # Uniform thickness of 2D element
    