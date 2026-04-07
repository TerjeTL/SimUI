from dataclasses import dataclass, field
from typing import Optional

import numpy as np


def _zeros(shape: int | tuple[int, ...], dtype=np.float32):
    return field(default_factory=lambda: np.zeros(shape, dtype=dtype))


@dataclass
class Frame:
    index: int = 0
    time: Optional[float] = None

    # submerged mesh
    vertices:     np.ndarray = _zeros((0, 3))
    indices:      np.ndarray = _zeros((0, 3), dtype=np.uint32)

    # per-face hydrostatic data (one entry per triangle)
    faceNormals:  np.ndarray = _zeros((0, 3))   # outward world-space normals
    faceCops:     np.ndarray = _zeros((0, 3))   # centre of pressure, world-space
    facePressure: np.ndarray = _zeros(0)        # hydrostatic pressure magnitude (Pa)

    # entity transform
    position:     np.ndarray = _zeros(3)        # world position
    rotation:     np.ndarray = field(           # row-major 3x3 rotation matrix
        default_factory=lambda: np.eye(3, dtype=np.float32).flatten()
    )
