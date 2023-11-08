import sys

import pygame as pg
from pygame import Vector2

from text_input import TextInput


pg.init()
screen = pg.display.set_mode(Vector2(800, 600))

clock = pg.time.Clock()
MAX_FPS = 60

text_input = TextInput()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill("White")
    text_input.render(screen)
    pg.display.flip()
    clock.tick(MAX_FPS)
