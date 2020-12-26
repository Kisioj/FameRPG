import pygame as pg
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE
from pygame.surface import Surface
from keyboard import keyboard
from talk_hud import TalkHUD
from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, PIXEL_HEIGHT, PIXEL_WIDTH

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
fake_screen = Surface((208, 208))

pg.display.set_caption('FAME RPG')
clock = pg.time.Clock()

# load map data

font = pg.font.Font("rsc/kongtext.ttf", 14)  # https://www.1001fonts.com/kongtext-font.html#styles


from world_map import START_MAP
from player import Player


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 0, pg.Color("white"))
    return fps_text


player = Player(x=14, y=7, current_map=START_MAP, filename='rsc/M_01.png', metadata_filename='rsc/hero_sprite_metadata.json')
talk_hud = TalkHUD(x=0, y=PIXEL_HEIGHT-48, width=PIXEL_WIDTH, height=48,
                   font_filename="rsc/kongtext.ttf", font_size=8, font_color="white")


def game_loop():
    game_exit = False
    while not game_exit:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
            elif event.type == pg.KEYDOWN:
                keyboard.add(event.key)

                if event.key == pg.K_z:
                    if talk_hud.is_open():
                        talk_hud.next_page()
                    else:
                        player.action(talk_hud)

            elif event.type == pg.KEYUP:
                keyboard.remove(event.key)

        if player.can_move() and not talk_hud.is_open():
            player.move()

        if player.should_teleport():
            player.teleport()

        pg.draw.rect(fake_screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        player.current_map.draw_layers(fake_screen, player.camera)
        player.draw(fake_screen, player.camera)
        player.current_map.draw_npcs(fake_screen, player.camera)
        player.current_map.draw_overlay_layers(fake_screen, player.camera)
        talk_hud.draw(fake_screen)

        pg.transform.scale2x(fake_screen, screen)

        screen.blit(update_fps(), (0, 0))
        pg.display.update()
        clock.tick(FPS)


game_loop()
pg.quit()
