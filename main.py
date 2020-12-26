import pygame as pg
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
from keyboard import keyboard


pg.init()

SCREEN_WIDTH = 416
SCREEN_HEIGHT = 416

white = (255, 255, 255)

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = Surface((208, 208))

pg.display.set_caption('FAME RPG')
clock = pg.time.Clock()

# load map data

font = pg.font.SysFont("Arial", 18)

from settings import FPS
from world_map import START_MAP
from player import Player


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


player = Player(x=10, y=0, current_map=START_MAP, filename='rsc/M_01.png', metadata_filename='rsc/hero_sprite_metadata.json')


def game_loop():
    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            elif event.type == pg.KEYDOWN:
                keyboard.add(event.key)
                if event.key == pg.K_z:
                    player.action()

            elif event.type == pg.KEYUP:
                keyboard.remove(event.key)

        if player.can_move():
            player.move()

        if player.should_teleport():
            player.teleport()

        pg.draw.rect(fake_screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        player.current_map.draw_layers(fake_screen, player.camera)
        player.draw(fake_screen, player.camera)
        player.current_map.draw_npcs(fake_screen, player.camera)
        player.current_map.draw_overlay_layers(fake_screen, player.camera)

        pg.transform.scale2x(fake_screen, screen)
        screen.blit(update_fps(), (10, 0))
        pg.display.update()
        clock.tick(FPS)


game_loop()
pg.quit()
