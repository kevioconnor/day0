from __future__ import annotations

from typing import TYPE_CHECKING
from numpy import e

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
from render_functions import render_bar, render_name_at_location

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass
        
    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)
        render_bar(console=console, current_val=self.player.fighter.hp,
        max_val=self.player.fighter.max_hp, total_width=20)
        render_name_at_location(console=console, x=21, y=44, engine=self)
