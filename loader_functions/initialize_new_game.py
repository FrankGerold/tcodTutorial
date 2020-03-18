import tcod

from components.fighter import Fighter
from components.inventory import Inventory

from entity import Entity

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder

from components.level import Level

from components.equipment import Equipment


def get_constants():

    window_title = 'Bluntlike'

    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': tcod.Color(0, 0, 102),
        'dark_ground': tcod.Color(0, 51, 102),
        'light_wall': tcod.Color(51, 0, 102),
        'light_ground': tcod.Color(51, 51, 102)
    }

    constants = {
        'window title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'map_width': map_width,
        'map_height': map_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'colors': colors
    }

    return constants

def get_game_variables(constants):

    fighter_component = Fighter(hp=100, defense=1, power=4)
    inventory_component = Inventory(16)
    level_component = Level()
    equipment_component = Equipment()

    player = Entity(int(constants['screen_width'] / 2), int(constants['screen_height'] / 2), '@', tcod.red,
                    'Player', blocks=True, fighter=fighter_component, render_order=RenderOrder.ACTOR,
                    inventory=inventory_component, level=level_component, equipment=equipment_component)
    entities = [player]

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'],
                      constants['room_max_size'], constants['map_width'],
                      constants['map_height'], player, entities,)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYER_TURN

    return player, entities, game_map, message_log, game_state