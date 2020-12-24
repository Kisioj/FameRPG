from time import perf_counter

from settings import TILE_WIDTH, TILE_HEIGHT


class Camera:
    def __init__(self, obj):
        self.obj = obj
        self.width = self.obj.view_range_x * 2 + 1
        self.height = self.obj.view_range_y * 2 + 1
        self.update()

    def update(self):
        self.top = self.obj.y - self.obj.view_range_y
        self.left = self.obj.x - self.obj.view_range_x
        self.bottom = self.top + self.height
        self.right = self.left + self.width

    def get_pixel_offset(self):
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
            return int(offset_x), int(offset_y)

