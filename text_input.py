from typing import Callable

import pygame as pg
from pygame import Surface, Vector2, Rect


class TextInput:
    def __init__(self, on_enter: Callable[..., None] = lambda: print("Enter pressed")):
        self.size = Vector2(140, 35)

        self.text = ""
        self._on_enter = on_enter

        self.has_focus = False
        self.input_rectangle = Rect(Vector2(0, 0), self.size)

        self.font = pg.font.Font(None, 50)
        self._input_color_passive = "Grey"
        self._input_color_active = "Blue"
        self.input_color = self._input_color_passive
        self.text_color = "Black"

    def listen_for_focus(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0] is True:
            if self.input_rectangle.collidepoint(mouse_pos):
                self.has_focus = True
                self.input_color = self._input_color_active
            else:
                self.has_focus = False
                self.input_color = self._input_color_passive

    def listen_for_text(self):
        self.listen_for_focus()
        if self.has_focus:
            event = pg.event.wait()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    self.text = ""
                    self._on_enter()
                else:
                    if event.unicode.isprintable():
                        self.text += event.unicode

    def update_text(self, screen: Surface):
        font_surface = self.font.render(self.text, True, self.text_color).convert_alpha()
        font_rectangle = font_surface.get_rect()

        self.input_rectangle = Rect(Vector2(0, 0), self.size)
        self.input_rectangle.center = screen.get_rect().center

        if font_rectangle.width > self.input_rectangle.width:
            self.input_rectangle.width = font_rectangle.width + 10
        else:
            self.input_rectangle.width = self.size.x

        self.input_rectangle.center = screen.get_rect().center
        font_rectangle.center = self.input_rectangle.center

        screen.blit(font_surface, font_rectangle)
        pg.draw.rect(screen, self.input_color, self.input_rectangle, 2)

    def render(self, screen: Surface):
        self.listen_for_text()
        self.update_text(screen)
