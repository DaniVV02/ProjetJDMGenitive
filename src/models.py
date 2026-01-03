from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Prep(str, Enum):
    DE = "DE"
    DES = "DES"
    DU = "DU"
    D = "D'"

class Article(str, Enum):
    LE = "LE"
    LA = "LA"
    LES = "LES"
    L = "L'"
    UN = "UN"
    UNE = "UNE"

class TermInfo(BaseModel):
    name: str

class RelationInstance(BaseModel):
    termA: TermInfo
    termB: TermInfo
    prep: Prep
    relation_type: str
    is_det: bool
    determinant: Optional[Article] = None

class Node(BaseModel):
    id_node: int
    node1: int
    node2: int
    weight: float

class ApiCall(BaseModel):
    id_relation: int
    relation_nodes: Dict[str, List[Node]] = Field(default_factory=dict)

class RelProto(BaseModel):
    gen_type: str
    termA: str
    termB: str
    nodes_a: Dict[int, float]
    nodes_b: Dict[int, float]
    fusion_number: int = 0

class Corpus(BaseModel):
    original_file: Optional[Path] = None
    data: Dict[str, RelationInstance] = Field(default_factory=dict)
