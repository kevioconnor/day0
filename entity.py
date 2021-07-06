from typing import Tuple

class Entity:
    """
    Represents players, items, enemies etc on the screen
    """
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        # Move entity by amount
        self.x += dx
        self.y += dy