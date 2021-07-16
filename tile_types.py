from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32), ("fg", "3B"), ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("walkable", np.bool), ("transparent", np.bool), ("dark", graphic_dt), ("light", graphic_dt)
    ]
)

def new_tile(
    *,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, transparent=True,
    dark=(ord(" "), (255, 255, 255), (25, 25, 25)),
    light=(ord(" "), (255, 255, 255), (140, 140, 140)),
)

wall = new_tile(
    walkable=False, transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (90, 90, 90)),
)
