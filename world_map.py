import pytmx
from pytmx import TiledObjectGroup

from settings import TILE_WIDTH, TILE_HEIGHT


class Teleport:
    def __init__(self, map_name, to_x, to_y):
        self.map_name = map_name
        self.to_x = to_x
        self.to_y = to_y


class WorldMap:
    def __init__(self, name):
        self.data = pytmx.load_pygame(f'rsc/{name}.tmx')
        self.dense_positions = set()
        self.teleport_positions = dict()
        self.layers = []
        self.overlay_layers = []
        for layer in self.data.visible_layers:
            if isinstance(layer, TiledObjectGroup):
                for obj in layer:
                    teleport = obj.properties.get('teleport')
                    if teleport:
                        map_name, to_x, to_y = teleport.split(',')
                        to_x = int(to_x)
                        to_y = int(to_y)
                        x = int(obj.x // TILE_WIDTH)
                        y = int(obj.y // TILE_HEIGHT)
                        self.teleport_positions[(x, y)] = Teleport(map_name, to_x, to_y)
                continue

            overlay = layer.properties.get('overlay', False)
            if overlay:
                self.overlay_layers.append(layer)
            else:
                self.layers.append(layer)

            for x, y, gid in layer:
                properties = self.data.get_tile_properties_by_gid(gid)
                if properties and properties.get('density'):
                    self.dense_positions.add((x, y))


    def draw(self, surface, camera, layers):
        from_x = max(camera.left - 1, 0)
        to_x = min(camera.right, self.data.width - 1)
        from_y = max(camera.top - 1, 0)
        to_y = min(camera.bottom, self.data.height - 1)

        offset_x, offset_y = camera.get_pixel_offset()

        for layer in layers:
            for x in range(from_x, to_x + 1):
                for y in range(from_y, to_y + 1):
                    gid = layer.data[y][x]
                    tile = self.data.get_tile_image_by_gid(gid)
                    if not tile:
                        continue

                    relative_x = x - camera.left
                    relative_y = y - camera.top

                    surface.blit(tile, (relative_x * TILE_WIDTH - offset_x, relative_y * TILE_HEIGHT - offset_y))

    def draw_layers(self, surface, camera):
        self.draw(surface, camera, self.layers)

    def draw_overlay_layers(self, surface, camera):
        self.draw(surface, camera, self.overlay_layers)


MAPS = {
    'world': WorldMap('world'),
    'forest': WorldMap('forest'),
}

START_MAP = MAPS['world']
