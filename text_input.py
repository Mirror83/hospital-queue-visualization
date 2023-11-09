from typing import Callable

import pygame as pg
from pygame import Surface, Vector2, Rect


class TextInput:
    def __init__(
            self,
            top_left: Vector2,
            size: Vector2 = Vector2(140, 35),
            font_size: int = 50,
            on_enter: Callable[..., None] = lambda: print("Enter pressed"),
            label_text=""
    ):
        self.size = size

        self.text = ""
        self.label_text = label_text

        self._on_enter = on_enter

        self._has_focus = False
        self.input_rectangle = Rect(top_left, self.size)

        self.font = pg.font.Font(None, font_size)
        self._input_color_passive = "Grey"
        self._input_color_active = "Blue"
        self.input_color = self._input_color_passive
        self.text_color = "Black"
        self.font_surface = self.font.render(self.text, True, self.text_color)
        self.font_rectangle = self.font_surface.get_rect()

    def listen_for_focus(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] is True:
            if self.input_rectangle.collidepoint(mouse_pos):
                self._has_focus = True
                self.input_color = self._input_color_active
            else:
                self._has_focus = False
                self.input_color = self._input_color_passive

    def has_focus(self):
        return self._has_focus

    def update_text(self, event_key: int, text: str):
        if event_key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            self.update_text_box_size()
        elif event_key == pg.K_RETURN:
            self.text = ""
            self._on_enter()
            self.update_text_box_size()
        else:
            if text.isprintable():
                self.text += text
                self.update_text_box_size()

    def update_text_box_size(self):
        self.font_surface = self.font.render(self.text, True, self.text_color).convert_alpha()
        self.font_rectangle = self.font_surface.get_rect()

        self.input_rectangle.width = max(self.size.x, self.font_rectangle.width + 20)
        self.font_rectangle.midleft = self.input_rectangle.midleft
        self.font_rectangle.x += 10

    def render(self, screen: Surface):
        self.listen_for_focus()

        screen.blit(self.font_surface, self.font_rectangle)
        pg.draw.rect(screen, self.input_color, self.input_rectangle, 2)
