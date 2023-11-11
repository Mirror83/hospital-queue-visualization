from typing import Callable

import pygame as pg
from pygame import Surface, Color, Vector2, Rect
from pygame.font import Font

from text_button import TextButton


class Dialog:
    def __init__(
            self,
            overlay_size: Vector2,
            message: str = "",
            on_dismiss: Callable[[], None] = lambda: print("Dismissed")):
        self.overlay_surface = Surface(overlay_size).convert_alpha()
        self.overlay_rect = self.overlay_surface.get_rect()
        self.overlay_color = Color(0, 0, 0, 155)
        self.overlay_surface.fill(self.overlay_color)

        self.dialog_box_surface = Surface(Vector2(500, 200)).convert_alpha()
        self.dialog_box_surface.fill(Color(0, 0, 0, 0))
        self.dialog_box_rect = self.dialog_box_surface.get_rect()
        self.dialog_box_rect.center = self.overlay_rect.center

        self.message = message

        self.font = Font(None, 30)
        self.text_color = "darkgrey"
        self.font_surface = self.font.render(self.message, True, self.text_color)
        self.font_rect = self.font_surface.get_rect()
        self.font_rect.center = self.convert_coords(
            Vector2(self.dialog_box_rect.topleft),
            Vector2(self.dialog_box_rect.center)
        )

        self.dismiss_button = TextButton(
            "Dismiss",
            Vector2(self.dialog_box_rect.size[0] - 100, 30),
            on_dismiss,
            25,
            "Black",
            offsets=Vector2(self.dialog_box_rect.topleft))

    def click_dismissed_button(self):
        self.dismiss_button.click()
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def set_message(self, message):
        self.message = message

    def set_font(self):
        self.font_surface = self.font.render(self.message, True, self.text_color)
        self.font_rect = self.font_surface.get_rect()
        self.font_rect.center = self.convert_coords(
            Vector2(self.dialog_box_rect.topleft),
            Vector2(self.dialog_box_rect.center)
        )

    @staticmethod
    def convert_coords(top_left: Vector2, coords: Vector2):
        return Vector2(coords.x - top_left.x, coords.y - top_left.y)

    def render(self, surface: Surface):
        self.set_font()
        # The overlay surface should cover the entire screen
        surface.blit(self.overlay_surface, Vector2(0, 0))

        self.overlay_surface.blit(self.dialog_box_surface, self.dialog_box_rect)

        pg.draw.rect(
            self.dialog_box_surface,
            "White",
            Rect(Vector2(0, 0), self.dialog_box_rect.size),
            0,
            20,
            20,
            20,
            20,
            20
        )

        self.dialog_box_surface.blit(self.font_surface, self.font_rect)
        self.dismiss_button.render(self.dialog_box_surface)
