import random
from typing import Iterator, Tuple
import tcod
from game_map import GameMap
import tile_types

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

def gen_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    rm_1 = RectRoom(x=20, y=15, width=10, height=15)
    rm_2 = RectRoom(x=35, y=15, width=10, height=15)
    dungeon.tiles[rm_1.inner] = tile_types.floor
    dungeon.tiles[rm_2.inner] = tile_types.floor

    return dungeon
