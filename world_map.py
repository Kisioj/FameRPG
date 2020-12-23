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


    def draw_layers(self, surface):
        for layer in self.layers:
            for x, y, gid in layer:
                tile = self.data.get_tile_image_by_gid(gid)
                if not tile:
                    continue
                surface.blit(tile, (x * TILE_WIDTH, y * TILE_HEIGHT))

    def draw_overlay_layers(self, surface):
        for layer in self.overlay_layers:
            for x, y, gid in layer:
                tile = self.data.get_tile_image_by_gid(gid)
                if not tile:
                    continue
                surface.blit(tile, (x * TILE_WIDTH, y * TILE_HEIGHT))

