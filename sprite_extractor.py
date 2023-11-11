import pygame as pg
from pygame import Surface, Vector2, Rect


class SpriteExtractor:
    """A class that can be used to extract individual images from a sprite sheet"""
    def __init__(self, sheet: Surface):
        """
        Creates an instance of SpriteExtractor
        :param sheet: A sprite sheet image loaded into pygame as a surface
        """
        self.sheet = sheet

    def extract_portion_from(self, top_left: Vector2, image_size: Vector2) -> Surface:
        """
        Extracts a portion of the sprite sheet
        :param top_left: The top left coordinate from which extraction begins
        :param image_size: The size of the area to be extracted

        :returns: A Surface representing the required portion of the sprite sheet
        """
        image_surface = Surface(image_size).convert_alpha()
        image_surface.set_colorkey("Black")
        image_surface.blit(self.sheet, Vector2(0, 0), Rect(top_left, image_size))

        return image_surface
