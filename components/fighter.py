from __future__ import annotations
from typing import TYPE_CHECKING
import color

from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, defence: int, attack: int):
        self.max_hp = hp
        self._hp = hp
        self.defence = defence
        self.attack = attack
    
    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()
    
    def die(self) -> None:
        if self.engine.player is self.parent:
            death_msg = "You died!"
            death_msg_color = color.player_die
        else: 
            death_msg = f"{self.parent.name} is dead!"
            death_msg_color = color.enemy_die
        
        self.parent.char = "X"
        self.parent.color = (200, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_msg, death_msg_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp = self.hp + amount

        if new_hp > self.max_hp:
            new_hp = self.max_hp

        hp_recovered = new_hp - self.hp

        self.hp = new_hp
        return hp_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount