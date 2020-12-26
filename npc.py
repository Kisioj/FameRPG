import json
from time import perf_counter

from camera import Camera
from settings import TILE_WIDTH, TILE_HEIGHT
import pygame as pg


class NPC:
    def __init__(self, x, y, current_map, filename, metadata_filename):
        self.x = x
        self.y = y
        self.current_map = current_map
        self.old_x = self.x
        self.old_y = self.y
        self.image = pg.image.load(filename)
        self.teleporting_to = None

        self.dir = 'DOWN'
        self.move_time = 0
        self.move_delay = 0.3  # in seconds
        self.view_range_x = 6
        self.view_range_y = 6

        with open(metadata_filename) as metadata_file:
            data = json.load(metadata_file)

        self.tile_width = data['tile_width']
        self.tile_height = data['tile_height']

        self.tiles = {
            tile_name: tile_position
            for tile_name, tile_position in data['tiles'].items()
        }

        self.animated_tiles = {
            tile_name: tile_positions
            for tile_name, tile_positions in data['animations'].items()
        }

    def _draw(self, surface, camera, offset_x, offset_y):
        relative_x = self.x - camera.left
        relative_y = self.y - camera.top
        pixel_x = relative_x * TILE_WIDTH
        pixel_y = relative_y * TILE_HEIGHT

        time_passed = perf_counter() - self.move_time
        if time_passed >= self.move_delay:
            tile_pos = self.tiles[self.dir]
        else:  # we are currently moving
            factor = time_passed / self.move_delay
            if factor < 0.5:
                frame = 0
            else:
                frame = 1
            tile_pos = self.animated_tiles[self.dir][frame]

        tile = [*tile_pos, self.tile_width, self.tile_height]

        surface.blit(
            self.image,
            (pixel_x - offset_x, pixel_y - offset_y),
            tile,
        )

    def draw(self, surface, camera):
        offset_x, offset_y = camera.get_pixel_offset(for_player=False)
        self._draw(surface, camera, offset_x, offset_y)
