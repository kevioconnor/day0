from __future__ import annotations
import copy
from typing import Optional
import tcod

from engine import Engine
import color, entity_factories, input_handlers
from procgen import gen_dungeon

background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> Engine:
    map_width = 80
    map_height = 40

    room_max_size = 10
    room_min_size = 6
    max_no_rooms = 30

    max_monster_per_room = 2
    max_item_per_room = 3

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    engine.game_map = gen_dungeon(
        max_no_rooms=max_no_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monster_per_room=max_monster_per_room,
        max_item_per_room=max_item_per_room,
        engine=engine
    )
    engine.update_fov()
    engine.message_log.add_message(
        "You are currently in Caveman Cave.", color.white
    )
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)
        console.print(console.width //2, console.height //2 -4, "DAY 0", fg=color.menu_title, alignment=tcod.CENTER)
        console.print(console.width //2, console.height -2, "by kevioconnor", fg=color.menu_title, alignment=tcod.CENTER)

        menu_width = 24
        for i, text in enumerate(["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            pass
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None           