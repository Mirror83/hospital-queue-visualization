import sys
from tkinter import messagebox

import pygame as pg
from pygame import Vector2

from priority_queue import AdaptablePriorityQueue
from text_button import TextButton
from text_input import TextInput


def on_add():
    try:
        key = int(text_input_list[0].text)
        value = text_input_list[1].text
        index_locator_dict[key] = pq.add(key, value)
        print(pq)
        print(index_locator_dict)

    except ValueError:
        if messagebox.showerror(
                "Invalid input",
                "Only pass in numeric values for key") == "ok":
            text_input_list[0].clear()


def on_update():
    try:
        old_key = int(text_input_list[2].text)
        new_key = int(text_input_list[3].text)
        pq.update(index_locator_dict[old_key], new_key, index_locator_dict[old_key].value)
        # TODO: Update index_locator_map

        print(pq)
        print(index_locator_dict)

    except ValueError:
        if messagebox.showerror("Invalid input", "Only pass in numeric values for key") == "ok":
            text_input_list[0].clear()


def insert(key, value):
    index_locator_dict[key] = pq.insert(key, value)


def remove(key):
    try:
        pq.remove(index_locator_dict[key])
        index_locator_dict.pop(key)
    except ValueError:
        print(f"The object with the key {key} does not exist")


pg.init()
pg.display.set_caption("hospital-queue-visualization")
screen = pg.display.set_mode(Vector2(1000, 700))

clock = pg.time.Clock()
MAX_FPS = 60

KEY_TEXT_INPUT_SIZE = Vector2(50, 30)
VALUE_TEXT_INPUT_SIZE = Vector2(100, 30)
text_input_list = [
    TextInput(top_left=Vector2(50, 400), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(150, 400), size=VALUE_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(50, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(150, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(50, 500), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(150, 500), size=VALUE_TEXT_INPUT_SIZE, font_size=30),
]

focused_input: TextInput | None = None
exists_focused_input = False

index_locator_dict: dict[int, AdaptablePriorityQueue.Locator] = dict()
pq = AdaptablePriorityQueue()

text_button_list = [
    TextButton(
        text="Add",
        top_left=Vector2(270, 400),
        on_click_handler=on_add,
        font_size=30,
        color="Blue"
    ),
    TextButton(
        text="Change priority",
        top_left=Vector2(270, 450),
        on_click_handler=on_add,
        font_size=30,
        color="Blue"
    ),
    TextButton(
        text="Remove",
        top_left=Vector2(270, 500),
        on_click_handler=on_add,
        font_size=30,
        color="Blue"
    ),
    TextButton(
        text="Remove min",
        top_left=Vector2(470, 400),
        on_click_handler=on_add,
        font_size=30,
        color="Blue"
    ),
    TextButton(
        text="Min",
        top_left=Vector2(470, 450),
        on_click_handler=on_add,
        font_size=30,
        color="Blue"
    )
]

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
