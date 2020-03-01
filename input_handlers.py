import tcod

def handle_keys(key):
    # Movement Keys
    if key.vk == tcod.KEY_UP:
        return {'move': (0, -1)}

    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0, 1)}

    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1, 0)}

    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter toggles full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # exit game
        return {'exit': True}

    # No key pressed
    return {}