from map_objects.tile import Tile

from map_objects.rectangle import Rect

from random import randint

import tcod

from entity import Entity

from components.ai import BasicMonster

from components.fighter import Fighter

from render_functions import RenderOrder

from components.item import Item

from components.inventory import Inventory

from item_functions import heal, lightning, fireball, confusion

from game_messages import Message

from components.stairs import Stairs

from random_utilities import random_choice_from_dict, from_dungeon_level

from components.equipment import EquipmentSlots

from components.equippable import Equippable


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in
                 range(self.width)]


        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height,
                 player, entities):

        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height of room
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # random position within map bounds
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)
            # Check if new room intersects with others
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # if room check didnt break, add new room to map tiles
                self.create_room(new_room)

                # center coord of room
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # if this is first room, player starts here
                    player.x = new_x
                    player.y = new_y


                else:
                    # for all rooms after first, connect to previous room with tunnel
                    # center coords of prev room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Flip a coin
                    if randint (0, 1) == 1:
                        # First move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # or vice versa
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        self.create_v_tunnel(prev_y, new_y, prev_x)

                self.place_entities(new_room, entities)

                # Finally, append new room to list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', tcod.white,
                             'Stairs Down', render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        # Walk through tiles in the given rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):

        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)

        # Get random # monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 35,
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level),

            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'breastplate': from_dungeon_level([[10, 6]], self.dungeon_level),
            'pantaloons': from_dungeon_level([[8, 5]], self.dungeon_level),
            'helmet': from_dungeon_level([[4, 3]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # choose rand location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 +1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):

                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    fighter_component: Fighter = Fighter(hp=20, defense=0, power=4, xp=35)

                    ai_component = BasicMonster()
                    inventory_component = Inventory(3)

                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True,
                                     fighter=fighter_component, ai=ai_component,
                                     render_order=RenderOrder.ACTOR, inventory=inventory_component)

                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()
                    inventory_component = Inventory(5)

                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True,
                                     fighter=fighter_component, ai=ai_component,
                                     render_order=RenderOrder.ACTOR, inventory=inventory_component)

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)

                    item = Entity(x, y, '!', tcod.violet, 'Health Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)

                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=fireball, damage=25, radius=3, targeting=True,
                                          targeting_message=Message('Click a target tile to cast a Fireball\
                                          , or right-click to cancel.', tcod.light_cyan))

                    item = Entity(x, y, '#', tcod.orange, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=confusion, targeting=True,
                                          targeting_message=Message('Click an enemy to confuse them!\
                                           Right-click/escape to cancel.', tcod.cyan))

                    item = Entity(x, y, '#', tcod.light_pink, 'Confusion Scroll',
                                  render_order=RenderOrder.ITEM, item=item_component)

                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=lightning, damage=40, maximum_range=5)

                    item = Entity(x, y, '#', tcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)

                    item = Entity(x, y, '/', tcod.sky, 'Greatsword', render_order=RenderOrder.ITEM,
                                  equippable=equippable_component)

                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=3)

                    item = Entity(x, y, '[', tcod.darker_orange, 'Kite Shield', render_order=RenderOrder.ITEM,
                                  equippable=equippable_component)

                elif item_choice == 'breastplate':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, hp_bonus=3)

                    item = Entity(x, y, 'M', tcod.dark_azure, 'Plate Mail Armor',
                                  render_order=RenderOrder.ITEM,
                                  equippable=equippable_component)

                elif item_choice == 'helmet':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, defense_bonus=2)

                    item = Entity(x, y, '0', tcod.dark_gray, 'Bucket Helmet',
                                  render_order=RenderOrder.ITEM,
                                  equippable=equippable_component)

                elif item_choice == 'pantaloons':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, hp_bonus=2, power_bonus=2)

                    item = Entity(x, y, 'n', tcod.dark_gray, 'Harlequin Pantaloons',
                                  render_order=RenderOrder.ITEM,
                                  equippable=equippable_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'],
                      constants['room_max_size'], constants['map_width'], constants['map_height'],
                      player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest and recover your strength...', tcod.yellow))

        return entities