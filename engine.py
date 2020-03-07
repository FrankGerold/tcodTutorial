import tcod
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates

def main():
    print('Suhh dude')

    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 3

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': tcod.Color(0, 0, 102),
        'dark_ground': tcod.Color(0, 51, 102),
        'light_wall': tcod.Color(51, 0, 102),
        'light_ground': tcod.Color(51, 51, 102)
    }
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.red, 'Player', True)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.blue, 'Rando', True)
    entities = [player, npc]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'Bluntlike', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYER_TURN

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius)

        # Old, Single render
        # tcod.console_set_default_foreground(con, tcod.red)
        # tcod.console_put_char(con, player.x, player.y, '@', tcod.BKGND_NONE)
        # tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        tcod.console_flush()

        # Without this, character wouldnt clear after movement, ended up snaking out. this clears previous spot.
        # tcod.console_put_char(con, player.x, player.y, ' ', tcod.BKGND_NONE)
        clear_all(con, entities) #removes character trails

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYER_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the face!')

                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if game_state ==GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYER_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
