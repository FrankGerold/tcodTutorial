from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        # tiles[30][22].blocked = True
        # tiles[30][22].block_sight = True
        # tiles[31][22].blocked = True
        # tiles[31][22].block_sight = True
        # tiles[32][22].blocked = True
        # tiles[32][22].block_sight = True

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, npc):
        # #Create 2 rooms for demo
        # room1 = Rect(20, 15, 10, 15)
        # room2 = Rect(35, 15, 10, 15)
        #
        # self.create_room(room1)
        # self.create_room(room2)
        #
        # self.create_h_tunnel(25, 40, 23)
        rooms = []
        num_rooms = 0
        for r in range(max_rooms):
            #random width and height of room
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            #random position within map bounds
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)
            #Check if new room intersects with others
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #if room check didnt break, add new room to map tiles
                self.create_room(new_room)

                #center coord of room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #if this is first room, player starts here
                    player.x = new_x
                    player.y = new_y

                # #placing npc in seconfd room
                # elif num_rooms == 1:
                #     npc.x = new_x
                #     npc.y = new_y

                else:
                    # for all rooms after first, connect to previous room with tunnel
                    #center coords of prev room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    #Flip a coin
                    if randint (0, 1) == 1:
                        #First move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        #or vice versa
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        self.create_v_tunnel(prev_y, new_y, prev_x)

                #Finally, append new room to list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        #Walk through tiles in the given rectangle and make them passable
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

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
