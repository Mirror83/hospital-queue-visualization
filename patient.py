import dataclasses

from pygame import Rect, Vector2, Surface
from pygame.font import Font


@dataclasses.dataclass
class PatientData:
    key: int
    name: str


class Patient:
    def __init__(self, data: PatientData, mid_bottom: Vector2, image: Surface):
        super().__init__()
        self.image = image
        self.data = data

        self.rect = Rect(Vector2(0, 0), self.image.get_size())
        self.rect.midbottom = mid_bottom

        self.font = Font(None, 30)
        self.text_color = "darkgrey"
        self.font_surface = self.font.render(f"({data.key}, {data.name})", True, self.text_color)
        self.font_rectangle = self.font_surface.get_rect()
        self.font_rectangle.midbottom = self.rect.midtop

    def init_font_surface(self, text: str):
        self.font_surface = self.font.render(text, True, self.text_color)

    def mid_bottom(self):
        return self.mid_bottom()

    def render(self, surface: Surface):
        self.init_font_surface(f"({self.data.key}, {self.data.name})")
        surface.blit(self.image, self.rect)
        surface.blit(self.font_surface, self.font_rectangle)
