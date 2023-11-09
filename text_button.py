from typing import Callable, Sequence

import pygame as pg
from pygame import Vector2, Rect, Cursor, SYSTEM_CURSOR_ARROW, SYSTEM_CURSOR_HAND, Surface, Color
from pygame.font import Font


class TextButton:
    def __init__(
            self,
            text: str,
            top_left: Vector2,
            on_click_handler: Callable[[], None],
            font_size: int,
            color: Color | int | str | tuple[int, int, int] | Sequence[int]
    ):
        self.text = text
        self.font = Font(None, font_size)
        self.default_color = color
        self.hover_color = "Purple"
        self.color = self.default_color

        self.font_surface = self.font.render(self.text, True, self.color).convert_alpha()
        self.rect = Rect(top_left, self.font_surface.get_size())

        self.on_click_handler = on_click_handler
        self.cursors = [Cursor(SYSTEM_CURSOR_ARROW), Cursor(SYSTEM_CURSOR_HAND)]
        self.cursor = self.cursors[0]

    def render(self, surface: Surface):
        self.check_hover()
        self.font_surface = self.font.render(self.text, True, self.color).convert_alpha()
        surface.blit(self.font_surface, self.rect)

    def is_hover(self):
        mouse_pos = Vector2(pg.mouse.get_pos())
        # mouse_pos.x -= Menu.MOUSE_OFFSET  # To account for positioning relative to menu Surface
        is_hover = self.rect.collidepoint(mouse_pos)
        return is_hover

    def check_hover(self):
        if self.is_hover():
            self.color = self.hover_color
            if self.cursor != self.cursors[1]:
                self.cursor = self.cursors[1]
                pg.mouse.set_cursor(self.cursor)
        else:
            self.color = self.default_color
            if self.cursor != self.cursors[0]:
                self.cursor = self.cursors[0]
                pg.mouse.set_cursor(self.cursor)

    def click(self):
        self.on_click_handler()
