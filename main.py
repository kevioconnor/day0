import copy
import tcod
import color

from engine import Engine
import entity_factories
from procgen import gen_dungeon

def main()-> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 40

    room_max_size = 10
    room_min_size = 6
    max_no_rooms = 30

    max_monster_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    
    engine.game_map = gen_dungeon(
        max_no_rooms=max_no_rooms, room_min_size=room_min_size, room_max_size=room_max_size,
        map_width=map_width, map_height=map_height, max_monster_per_room=max_monster_per_room, engine=engine
    )

    engine.update_fov()
    engine.message_log.add_message(
        "You are currently in Caveman Cave.", color.white
    )

    with tcod.context.new_terminal(
        screen_width, screen_height, tileset=tileset, title="Day0", vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            engine.event_handler.handle_events()

if __name__ == "__main__":
    main()