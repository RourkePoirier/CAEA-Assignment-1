from dataclasses import dataclass
from typing import Tuple
from enum import Enum

class VertexType(Enum):
    NORMAL = 1
    FIXED = 2
    FORCE = 3

@dataclass
class Vertex:
    x: float
    y: float
    type: VertexType

@dataclass
class Line:
    start: Vertex
    end: Vertex

@dataclass
class Triangle:
    verticies: Tuple[Vertex, Vertex, Vertex]

@dataclass
class ForceVector:
    vertex: Vertex
    angle_deg: float
    magnitude: float