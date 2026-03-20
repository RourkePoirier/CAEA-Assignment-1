from dataclasses import dataclass
from typing import Tuple
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
    verticies: Tuple[Node, Node, Node]

@dataclass
class ForceVector:
    node: Node
    angle_deg: float
    magnitude: float