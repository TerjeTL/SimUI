from dataclasses import dataclass


@dataclass
class Frame:
    boxPosition: tuple[float, float, float] = (0.0, 0.0, 0.0)
