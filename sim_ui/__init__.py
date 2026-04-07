from __future__ import annotations
from typing import TYPE_CHECKING

from sim_ui.simdata import Frame

if TYPE_CHECKING:
    from sim_ui.ui import SimUI

def __getattr__(name: str) -> object:
    if name == 'SimUI':
        from sim_ui.ui import SimUI
        return SimUI
    raise AttributeError(f"module 'sim_ui' has no attribute {name!r}")

__all__ = ['SimUI', 'Frame']
