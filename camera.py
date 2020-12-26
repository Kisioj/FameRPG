from time import perf_counter

import settings
from settings import TILE_WIDTH, TILE_HEIGHT


class Camera:
    def __init__(self, obj, world_width, world_height):
        self.obj = obj
        self.world_width = world_width
        self.world_height = world_height

        self.width = self.obj.view_range_x * 2 + 1
        self.height = self.obj.view_range_y * 2 + 1

        self.stopped_x = False
        self.stopped_y = False
        self.old_stopped_x = False
        self.old_stopped_y = False
        self.update()

    def update(self, world_width=None, world_height=None):
        if world_width:
            self.world_width = world_width
        if world_height:
            self.world_height = world_height

        self.old_stopped_x = self.stopped_x
        self.old_stopped_y = self.stopped_y
        self.stopped_x = False
        self.stopped_y = False

        self.top = self.obj.y - self.obj.view_range_y
        self.left = self.obj.x - self.obj.view_range_x

        if settings.FREEZE_CAMERA_ON_EDGE:
            if self.top < 0:
                self.top = 0
                self.stopped_y = True
            if self.left < 0:
                self.left = 0
                self.stopped_x = True

        self.bottom = self.top + self.height
        self.right = self.left + self.width

        if settings.FREEZE_CAMERA_ON_EDGE:
            if self.bottom > self.world_height:
                self.bottom = self.world_height
                self.top = self.bottom - self.height
                self.stopped_y = True

            if self.right > self.world_width:
                self.right = self.world_width
                self.left = self.right - self.width
                self.stopped_x = True


    def get_pixel_offset(self, for_player=False):
        obj = self.obj

        time_passed = perf_counter() - obj.move_time
        if time_passed >= obj.move_delay:
            return 0, 0
        else:  # we are currently moving
            old_pixel_x = obj.old_x * TILE_WIDTH
            old_pixel_y = obj.old_y * TILE_HEIGHT
            pixel_x = obj.x * TILE_WIDTH
            pixel_y = obj.y * TILE_HEIGHT

            factor = time_passed / obj.move_delay
            diff_x = pixel_x - old_pixel_x
            diff_y = pixel_y - old_pixel_y

            offset_x = (old_pixel_x + diff_x * factor) - pixel_x
            offset_y = (old_pixel_y + diff_y * factor) - pixel_y

            if for_player:
                offset_x = -offset_x
                offset_y = -offset_y
                if not(self.stopped_x or self.old_stopped_x):
                    offset_x = 0

                if not(self.stopped_y or self.old_stopped_y):
                    offset_y = 0
            else:
                if self.stopped_x or self.old_stopped_x:
                    offset_x = 0

                if self.stopped_y or self.old_stopped_y:
                    offset_y = 0

            return offset_x, offset_y

