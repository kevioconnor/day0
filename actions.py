from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING
import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self, engine) -> None:
        raise NotImplementedError()
        
class WaitAction(Action):
    def perform(self) -> None:
        pass

class EscapeAction(Action):
    def perform(self, engine) -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int) -> None:
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
        
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return actor at action's destination"""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError

class AttackAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return # Nothing to attack
        
        damage = self.entity.fighter.attack - target.fighter.defence
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} HP!", attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but nothing happens.", attack_color)
            
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
        if self.target_actor:
            return AttackAction(self.entity, self.dx, self.dy).perform()
        
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()