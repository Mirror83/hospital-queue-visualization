from enum import Enum, auto
from typing import Sequence

from pygame import Rect, Surface, Color, Vector2
from pygame.font import Font


class Label:
    class Alignment(Enum):
        LEFT = auto(),
        RIGHT = auto(),
        CENTER = auto()

    def __init__(
            self,
            text: str,
            rect: Rect,
            padding_top: int = 0,
            font_size: int = 20,
            color: Color | int | str | tuple[int, int, int] | Sequence[int] = "Grey",
            alignment: Alignment = Alignment.LEFT
    ):
        self.text = text
        self.color = color
        self.font = Font(None, font_size)
        self.font_surface = self.font.render(self.text, True, self.color)

        self.rect = Rect(Vector2(0, 0), self.font_surface.get_size())
        self.padding_top = padding_top

        match alignment:
            case self.Alignment.LEFT:
                self.rect.topleft = rect.topleft
            case self.Alignment.RIGHT:
                self.rect.topright = rect.topright
            case self.Alignment.CENTER:
                self.rect.midtop = rect.midtop

        self.rect.y += padding_top

    def render(self, surface: Surface):
        surface.blit(self.font_surface, self.rect)
