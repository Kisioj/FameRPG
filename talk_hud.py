import math
from time import perf_counter

from settings import PIXEL_WIDTH, PIXEL_HEIGHT
import pygame as pg
import pygame.gfxdraw


class TalkHUD:
    def __init__(self, x, y, width, height, font_filename, font_size, font_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_filename = font_filename
        self.font_size = font_size
        self.font_color = pg.Color(font_color)
        self.font = pg.font.Font(font_filename, font_size)

        # self.text = '''
        # A short poem may be a stylistic choice or it may be that you have said what you intended to say in a more concise way. Either way, they differ stylistically from a long poem in that there tends to be more care in word choice. Since there are fewer words people tend to spend more time on choosing a word that fits the subject to perfection. Because of this meticulous attitude, writing a short poem is often more tedious than writing a long poem.
        # '''.strip()
        self.text = ''
        self.pages_count = int(math.ceil(len(self.text) / 75))
        self.render_character_delay = 0.03


        self.next_page_icon_toggle_time = 0
        self.show_next_page_icon = True


    def open(self):
        self.rendered_characters = 0
        self.next_character_render_time = perf_counter()

    def are_all_characters_rendered(self):
        return self.rendered_characters == self.max_characters_on_current_page

    def is_open(self):
        return len(self.text) > 0

    def draw(self, surface):
        if not self.text:
            return

        if perf_counter() > self.next_page_icon_toggle_time:
            self.next_page_icon_toggle_time = perf_counter() + 0.25
            self.show_next_page_icon = not self.show_next_page_icon

        background = pg.Surface((self.width, self.height), pg.SRCALPHA)
        background.fill((0, 0, 0, 200))
        surface.blit(background, (self.x, self.y))

        while perf_counter() > self.next_character_render_time and not self.are_all_characters_rendered():
            self.next_character_render_time += self.render_character_delay
            self.rendered_characters += 1

        text = self.text[:self.rendered_characters]

        lines_count = int(math.ceil(len(text) / 25))
        for line_nr in range(lines_count):
            y = self.y + 6 + (line_nr * 14)
            line_text = text[line_nr*25:(line_nr+1)*25]
            font_surface = self.font.render(line_text, 0, self.font_color)
            surface.blit(font_surface, (self.x + 4, y))

        if self.pages_count > 1 and self.are_all_characters_rendered() and self.show_next_page_icon:
            pg.gfxdraw.filled_trigon(surface, 201, 202, 205, 202, 203, 204, (255, 255, 255))

    def set_text(self, text):
        self.text = text
        self.pages_count = int(math.ceil(len(self.text) / 75))
        self.max_characters_on_current_page = max(len(self.text), 25)

    def next_page(self):
        self.set_text(self.text[75:])
        self.rendered_characters = 0
        self.next_character_render_time = perf_counter()

