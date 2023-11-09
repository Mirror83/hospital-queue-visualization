import sys

import pygame as pg
from pygame import Vector2

from priority_queue import AdaptablePriorityQueue
from text_button import TextButton
from text_input import TextInput

pg.init()
screen = pg.display.set_mode(Vector2(1000, 600))

clock = pg.time.Clock()
MAX_FPS = 60

text_input_list = [
    TextInput(top_left=Vector2(150, 100), size=Vector2(50, 30), font_size=30),
    TextInput(top_left=Vector2(250, 100), size=Vector2(100, 30), font_size=30)
]

focused_input: TextInput | None = None
exists_focused_input = False

text_button_list = [
    TextButton(
        text="Add",
        top_left=Vector2(10, 100),
        on_click_handler=lambda: print("Clicked"),
        font_size=30
    )
]

index_locator_dict: dict[int, AdaptablePriorityQueue.Locator] = dict()
pq = AdaptablePriorityQueue()


def insert(key, value):
    index_locator_dict[key] = pq.insert(key, value)


def remove(key):
    try:
        pq.remove(index_locator_dict[key])
        index_locator_dict.pop(key)
    except ValueError as e:
        print("The object with this key does not exist")


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if focused_input is not None:
                focused_input.update_text(event.key, event.unicode)

        if event.type == pg.MOUSEBUTTONUP:
            for button in text_button_list:
                if event.button == pg.BUTTON_LEFT and button.is_hover():
                    button.click()

    screen.fill("White")
    for text_input in text_input_list:
        if text_input.has_focus():
            exists_focused_input = True
            focused_input = text_input

        text_input.render(screen)

    if not exists_focused_input:
        focused_input = None

    for button in text_button_list:
        button.render(screen)

    pg.display.flip()
    clock.tick(MAX_FPS)
