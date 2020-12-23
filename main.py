from collections import defaultdict
from time import perf_counter

import pygame as pg
import pytmx
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface

from settings import TILE_WIDTH, TILE_HEIGHT, FPS
from world_map import WorldMap

pg.init()

display_width = 800
display_height = 800




white = (255, 255, 255)

screen = pg.display.set_mode((display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = Surface((400, 400))

pg.display.set_caption('FAME RPG')
clock = pg.time.Clock()

# load map data
MAPS = {
    'world': WorldMap('world'),
    'forest': WorldMap('forest'),
}
current_map = MAPS['world']


font = pg.font.SysFont("Arial", 18)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.old_x = self.x
        self.old_y = self.y
        self.image = pg.image.load('rsc/M_01.png')

        self.dir = 'DOWN'
        self.move_time = 0
        self.move_delay = 0.3  # in seconds

        self.tiles = {
            'DOWN': (0, 0, TILE_WIDTH, TILE_HEIGHT),
            'RIGHT': (16, 0, TILE_WIDTH, TILE_HEIGHT),
            'UP': (32, 0, TILE_WIDTH, TILE_HEIGHT),
            'LEFT': (48, 0, TILE_WIDTH, TILE_HEIGHT),
        }
        self.animated_tiles = {
            'DOWN': [
                (0, 16, TILE_WIDTH, TILE_HEIGHT),
                (0, 32, TILE_WIDTH, TILE_HEIGHT),
            ],
            'RIGHT': [
                (16, 16, TILE_WIDTH, TILE_HEIGHT),
                (16, 32, TILE_WIDTH, TILE_HEIGHT),
            ],
            'UP': [
                (32, 16, TILE_WIDTH, TILE_HEIGHT),
                (32, 32, TILE_WIDTH, TILE_HEIGHT),
            ],
            'LEFT': [
                (48, 16, TILE_WIDTH, TILE_HEIGHT),
                (48, 32, TILE_WIDTH, TILE_HEIGHT),
            ]
        }

    def draw(self, surface):
        old_pixel_x = self.old_x * TILE_WIDTH
        old_pixel_y = self.old_y * TILE_HEIGHT
        pixel_x = self.x * TILE_WIDTH
        pixel_y = self.y * TILE_HEIGHT

        time_passed = perf_counter() - self.move_time
        if time_passed >= self.move_delay:
            new_pixel_x = pixel_x
            new_pixel_y = pixel_y
            tile = self.tiles[self.dir]
        else:  # we are currently moving
            factor = time_passed / self.move_delay
            diff_x = pixel_x - old_pixel_x
            diff_y = pixel_y - old_pixel_y
            new_pixel_x = old_pixel_x + diff_x * factor
            new_pixel_y = old_pixel_y + diff_y * factor

            if factor < 0.5:
                frame = 0
            else:
                frame = 1
            tile = self.animated_tiles[self.dir][frame]

        surface.blit(
            self.image,
            (new_pixel_x, new_pixel_y),
            tile,
        )

    def can_move(self):
        return perf_counter() > self.move_time + self.move_delay

    def move(self):
        global current_map

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
            if (new_x, new_y) in current_map.dense_positions:
                return

            if (new_x, new_y) in current_map.teleport_positions:
                teleport = current_map.teleport_positions[(new_x, new_y)]
                new_x = teleport.to_x
                new_y = teleport.to_y
                self.old_x = new_x
                self.old_y = new_y
                self.move_time = perf_counter()
                self.x, self.y = new_x, new_y
                current_map = MAPS[teleport.map_name]
            else:
                self.old_x = self.x
                self.old_y = self.y
                self.move_time = perf_counter()
                self.x, self.y = new_x, new_y




player = Player(x=1, y=1)
keyboard = set()


def game_loop():
    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            elif event.type == pg.KEYDOWN:
                keyboard.add(event.key)
            elif event.type == pg.KEYUP:
                keyboard.remove(event.key)

        if player.can_move():
            player.move()

        current_map.draw_layers(fake_screen)
        player.draw(fake_screen)
        current_map.draw_overlay_layers(fake_screen)

        pg.transform.scale2x(fake_screen, screen)
        screen.blit(update_fps(), (10, 0))
        pg.display.update()
        clock.tick(FPS)

game_loop()
pg.quit()
