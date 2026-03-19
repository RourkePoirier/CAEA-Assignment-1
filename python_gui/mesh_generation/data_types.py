from dataclasses import dataclass
from typing import Tuple

@dataclass
class Vertex:
    x: float
    y: float

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