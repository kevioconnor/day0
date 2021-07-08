from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for ev in events:
            action = self.event_handler.dispatch(ev)

            if action is None:
                continue

            action.perform(self, self.player)
    
    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for en in self.entities:
            console.print(en.x, en.y, en.char, fg=en.color)

        context.present(console)
        console.clear()
