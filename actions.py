from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self, engine) -> None:
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int) -> None:
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Return this action's destination"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at action's destination"""
        return self.engine.game_map.get_blocking_entity(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError

class AttackAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.blocking_entity
        if not target:
            return # Nothing to attack
        print(f"You punch {target.name}, winding it up a bit.")

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked by tile
        if self.engine.game_map.get_blocking_entity(dest_x, dest_y):
            return # Destination blocked by entity

        self.entity.move(self.dx, self.dy)

class CollideAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return AttackAction(self.entity, self.dx, self.dy).perform()
        
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()