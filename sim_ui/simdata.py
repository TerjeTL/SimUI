import base64
import dataclasses
from dataclasses import dataclass, field
from typing import Annotated, Optional

import numpy as np

# dtype tags — read by generate.py to emit the correct TS typed-array types
F32 = Annotated[np.ndarray, 'f32']
U32 = Annotated[np.ndarray, 'u32']


def _zeros(shape: int | tuple[int, ...], dtype=np.float32):
    return field(default_factory=lambda: np.zeros(shape, dtype=dtype))


@dataclass
class Frame:
    index: int = 0
    time: Optional[float] = None

    # full hull mesh (world-space, wireframe overlay) — optional
    hullVertices: Optional[F32] = None   # Nx3 float32
    hullIndices:  Optional[U32] = None   # Mx3 uint32

    # water surface mesh (world-space, blue wireframe) — optional
    waterVertices: Optional[F32] = None  # Nx3 float32
    waterIndices:  Optional[U32] = None  # Mx3 uint32

    # above-water (aero) mesh — optional
    aeroVertices: Optional[F32] = None   # Nx3 float32
    aeroIndices:  Optional[U32] = None   # Mx3 uint32

    # rig geometry (world-space) — optional
    mastPoints: Optional[F32] = None   # (2, 3) float32: [foot, tip]
    boomPoints: Optional[F32] = None   # (2, 3) float32: [root, tip]

    # sail strip mesh (world-space) — optional (n strips × 4 verts, 2 tris)
    sailStripVertices: Optional[F32] = None  # (n*4, 3) float32
    sailStripIndices:  Optional[U32] = None  # (n*2, 3) uint32

    # aero force vectors per strip (world-space) — optional
    sailForceOrigins: Optional[F32] = None  # (n, 3) float32
    sailForceVectors: Optional[F32] = None  # (n, 3) float32

    # foil (keel/rudder) strip mesh (world-space) — optional
    foilStripVertices: Optional[F32] = None  # (n*4, 3) float32
    foilStripIndices:  Optional[U32] = None  # (n*2, 3) uint32

    # foil force vectors per strip (world-space) — optional
    foilForceOrigins: Optional[F32] = None  # (n, 3) float32
    foilForceVectors: Optional[F32] = None  # (n, 3) float32

    # submerged mesh
    vertices:     F32 = _zeros((0, 3))
    indices:      U32 = _zeros((0, 3), dtype=np.uint32)

    # per-face hydrostatic data (one entry per triangle)
    faceNormals:  F32 = _zeros((0, 3))
    faceCops:     F32 = _zeros((0, 3))
    facePressure: F32 = _zeros(0)

    # entity transform
    position:     F32 = _zeros(3)
    rotation:     F32 = field(
        default_factory=lambda: np.eye(3, dtype=np.float32).flatten()
    )

    def to_wire(self) -> dict:
        """Serialize to JSON-safe dict: numpy arrays become base64 strings."""
        out = {}
        for f in dataclasses.fields(self):
            val = getattr(self, f.name)
            if val is None:
                continue
            if isinstance(val, np.ndarray):
                out[f.name] = base64.b64encode(val.tobytes()).decode()
            else:
                out[f.name] = val
        return out
