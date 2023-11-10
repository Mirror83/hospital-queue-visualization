import dataclasses

from pygame import Rect, Vector2, Surface
from pygame.font import Font
import pygame as pg


@dataclasses.dataclass
class PatientData:
    key: int
    name: str


class Patient:
    def __init__(self, data: PatientData, mid_bottom: Vector2):
        super().__init__()
        self.data = data
        self.size = Vector2(50, 100)

        self.rect = Rect((0, 0), self.size)
        self.rect.midbottom = mid_bottom
        self.rect_color = "Red"

        self.font = Font(None, 30)
        self.text_color = "Black"
        self.font_surface = self.font.render(f"({data.key}, {data.name})", True, self.text_color)
        self.font_rectangle = self.font_surface.get_rect()
        self.font_rectangle.midbottom = self.rect.midtop

    def init_font_surface(self, text: str):
        self.font_surface = self.font.render(text, True, self.text_color)

    def mid_bottom(self):
        return self.mid_bottom()

    def render(self, surface: Surface):
        self.init_font_surface(f"({self.data.key}, {self.data.name})")
        pg.draw.rect(surface, self.rect_color, self.rect)
        surface.blit(self.font_surface, self.font_rectangle)
