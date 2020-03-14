import math
import tcod
from render_functions import RenderOrder
from components.inventory import Inventory

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None, render_order=RenderOrder.CORPSE, item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.render_order = render_order
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # Move entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        dest_x = self.x + dx
        dest_y = self.y + dy

        if not (game_map.is_blocked(dest_x, dest_y) or get_blocking_entities_at_location(entities, dest_x, dest_y)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        return math.sqrt((x-self.x) ** 2 + (y - self.y) ** 2)

    # A* Search Algorithm - O(b^d) space and performance complexity
    def move_astar(self, target, entities, game_map):
        #Generate FOV map with same dimensions as game map
        fov = tcod.map_new(game_map.width, game_map.height)

        # scan current map each turn, set walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)

        # Scan all objects to see if they must be navigated around
        # also make sure object isnt self or target so that start and end points are free
        # AI class handles situation when self is next to target, wont need A* anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                #set tile as a wall to be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* Path
        # 1.41 is normal diagonal cost of moving (Sqrt of 2, hypotenuse of 1 length isosceles right triangle), can be 0.0 if diag moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute path between self coords and target coords
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if path exists, and, in this case, if its under 25 tiles
        # Path size matters if you want monsters to use alternative longer paths (for example thru other rooms) if, for example, the player is in a corridor
        # Makes sense to limit path size to prevent monsters running all around the map if alt path is far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # find next coords in computed path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # set self coords to next path tile
                self.x = x
                self.y = y

        else:
            # keep old move func as backup so that even if path doesnt exist (ex if another monster blocks a corridor) it will still move in the right general direction (closer to the player, towards corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

        # Delete path to free memory
        tcod.path_delete(my_path)






def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
