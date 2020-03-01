import tcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all

def main():
    print('Suhh dude')

    screen_width = 80
    screen_height = 50

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.red)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', tcod.blue)
    entities = [player, npc]

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = tcod.console_new(screen_width, screen_height)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Old, Single render
        # tcod.console_set_default_foreground(con, tcod.red)
        # tcod.console_put_char(con, player.x, player.y, '@', tcod.BKGND_NONE)
        # tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        render_all(con, entities, screen_width, screen_height)
        tcod.console_flush()

        # Without this, character wouldnt clear after movement, ended up snaking out. this clears previous spot.
        # tcod.console_put_char(con, player.x, player.y, ' ', tcod.BKGND_NONE)
        clear_all(con, entities) #removes character trails

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
