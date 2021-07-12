from __future__ import annotations
import random
from typing import Iterator, List, Tuple, TYPE_CHECKING
import tcod
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)
        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Returns inner area of room as 2D array"""
        return slice(self.x1 + 1, self.x2), slice(self.y1, self.y2)

def intersect(self, other: RectRoom) -> bool:
    """True if room overlaps with another room"""
    return (
        self.x1 <= other.x2
        and self.x2 >= other.x1
        and self.y1 <= other.y2
        and self.y2 >= other.y1
    )

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Returns a tunnel between two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2
    
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def gen_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    rm_1 = RectRoom(x=20, y=15, width=10, height=15)
    rm_2 = RectRoom(x=35, y=15, width=10, height=15)
    dungeon.tiles[rm_1.inner] = tile_types.floor
    dungeon.tiles[rm_2.inner] = tile_types.floor

    for x, y in tunnel_between(rm_2.center, rm_1.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon
