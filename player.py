from time import perf_counter
import pygame as pg

from camera import Camera
from keyboard import keyboard
from npc import NPC
from world_map import MAPS


class Player(NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.camera = Camera(self, world_width=self.current_map.data.width, world_height=self.current_map.data.height)

    def action(self):
        x, y = self.x, self.y

        if self.dir == 'UP':
            y -= 1
        elif self.dir == 'DOWN':
            y += 1
        elif self.dir == 'LEFT':
            x -= 1
        elif self.dir == 'RIGHT':
            x += 1

        print('action')

        for npc in self.current_map.npcs:
            if (x, y) == (npc.x, npc.y):
                npc.talk(self)



    def should_teleport(self):
        return self.teleporting_to and perf_counter() > self.move_time + self.move_delay

    def teleport(self):
        teleport = self.teleporting_to
        new_x = teleport.to_x
        new_y = teleport.to_y
        self.old_x = new_x
        self.old_y = new_y
        # self.move_time = perf_counter()
        self.x, self.y = new_x, new_y
        self.current_map = MAPS[teleport.map_name]
        self.teleporting_to = None
        self.camera.update(world_width=self.current_map.data.width, world_height=self.current_map.data.height)

    def can_move(self):
        return not self.teleporting_to and perf_counter() > self.move_time + self.move_delay

    def move(self):
        new_x, new_y, new_dir = self.x, self.y, self.dir
        if pg.K_UP in keyboard:
            new_dir = 'UP'
            new_y -= 1
        if pg.K_DOWN in keyboard:
            new_dir = 'DOWN'
            new_y += 1
        if pg.K_LEFT in keyboard:
            new_dir = 'LEFT'
            new_x -= 1
        if pg.K_RIGHT in keyboard:
            new_dir = 'RIGHT'
            new_x += 1

        if (new_x, new_y, new_dir) != (self.x, self.y, self.dir):
            self.dir = new_dir
            if not 0 <= new_x < self.current_map.data.width or not 0 <= new_y < self.current_map.data.height:
                return

            if (new_x, new_y) in self.current_map.dense_positions:
                return

            for npc in self.current_map.npcs:
                if (new_x, new_y) == (npc.x, npc.y):
                    return

            if (new_x, new_y) in self.current_map.teleport_positions:
                self.teleporting_to = self.current_map.teleport_positions[(new_x, new_y)]

            self.old_x = self.x
            self.old_y = self.y
            self.move_time = perf_counter()
            self.x, self.y = new_x, new_y
            self.camera.update()

    def draw(self, surface, camera):
        offset_x, offset_y = camera.get_pixel_offset(for_player=True)
        self._draw(surface, camera, offset_x, offset_y)