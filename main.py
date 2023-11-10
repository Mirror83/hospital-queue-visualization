import sys
from tkinter import messagebox

import pygame as pg
from pygame import Vector2, Rect

from label import Label
from priority_queue import AdaptablePriorityQueue
from text_button import TextButton
from text_input import TextInput


def update_key_locator_dict():
    key_locator_dict.clear()
    for locator in pq.locators():
        key_locator_dict[locator.key] = locator


def print_updates(tag: str = ""):
    if tag:
        print(f"{tag}: {pq}")
        print(f"{tag}: sequential - {pq.string_sequential()}")
        print(f"{tag}: {key_locator_dict}")
    else:
        print(pq)
        print("sequential - " + pq.string_sequential())
        print(key_locator_dict)


def on_add():
    try:
        key = int(text_inputs[0].text)
        value = text_inputs[1].text
        key_locator_dict[key] = pq.add(key, value)
        print_updates(tag="on_add")

        text_inputs[0].clear()
        text_inputs[1].clear()

    except ValueError:
        if messagebox.showerror(
                "Invalid input",
                "Key should be an integer") == "ok":
            text_inputs[0].clear()


def on_update():
    try:
        if not pq.is_empty():
            old_key = int(text_inputs[2].text)
            new_key = int(text_inputs[3].text)
            pq.update(key_locator_dict[old_key], new_key, key_locator_dict[old_key].value)
            update_key_locator_dict()
            print_updates(tag="on_update")

            text_inputs[2].clear()
            text_inputs[3].clear()
        else:
            print(f"change_priority: The queue is empty!")

    except ValueError:
        if messagebox.showerror("Invalid input", "Key should be an integer") == "ok":
            text_inputs[2].clear()
            text_inputs[3].clear()

    except KeyError:
        if messagebox.showerror("Invalid key", "There is no member with the key given") == "ok":
            text_inputs[2].clear()
            text_inputs[3].clear()


def on_remove():
    try:
        if not pq.is_empty():
            key = int(text_inputs[4].text)
            pq.remove(key_locator_dict[key])
            update_key_locator_dict()
            print_updates(tag="on_remove")

            text_inputs[4].clear()
        else:
            print("on_remove: There is nothing to remove!")

    except ValueError:
        if messagebox.showerror("Invalid input", "Key should be an integer") == "ok":
            text_inputs[4].clear()

    except KeyError:
        if messagebox.showerror("Invalid key", "There is no member with the key given") == "ok":
            text_inputs[2].clear()
            text_inputs[3].clear()


def on_remove_min():
    if not pq.is_empty():
        pq.remove_min()
        update_key_locator_dict()
        print_updates(tag="on_remove_min")
    else:
        print("There is nothing to remove!")


def on_min():
    if not pq.is_empty():
        print(f"min={key_locator_dict[pq.min()[0]]}")
    else:
        print("min: The queue is empty!")


def on_len():
    print(f"len={len(pq)}")


def on_is_empty():
    print(f"is_empty={pq.is_empty()}")


pg.init()
pg.display.set_caption("hospital-queue-visualization")
SCREEN_SIZE = Vector2(800, 600)

screen = pg.display.set_mode(SCREEN_SIZE)

sky_surface = pg.image.load("./assets/graphics/sky.png")
sky_rectangle = sky_surface.get_rect()
sky_rectangle.topleft = Vector2(0, 0)

clock = pg.time.Clock()
MAX_FPS = 60

KEY_TEXT_INPUT_SIZE = Vector2(50, 30)
VALUE_TEXT_INPUT_SIZE = Vector2(100, 30)
text_inputs = [
    TextInput(top_left=Vector2(50, 400), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(120, 400), size=VALUE_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(50, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(120, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(50, 500), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(120, 500), size=VALUE_TEXT_INPUT_SIZE, font_size=30),
]

label_text_list = ["key", "value", "key", "new key", "key", "value"]
labels = []

for i in range(len(text_inputs)):
    rect = Rect(Vector2(0, 0), Vector2(text_inputs[i].size))
    rect.topleft = text_inputs[i].input_rectangle.bottomleft
    labels.append(Label(label_text_list[i], rect))

focused_input: TextInput | None = None
exists_focused_input = False

key_locator_dict: dict[int, AdaptablePriorityQueue.Locator] = dict()
pq = AdaptablePriorityQueue()

text_buttons = [
    TextButton(
        text="Add",
        top_left=Vector2(250, 400),
        on_click_handler=on_add,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="Change priority",
        top_left=Vector2(250, 450),
        on_click_handler=on_update,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="Remove",
        top_left=Vector2(250, 500),
        on_click_handler=on_remove,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="Remove min",
        top_left=Vector2(450, 400),
        on_click_handler=on_remove_min,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="Min",
        top_left=Vector2(450, 450),
        on_click_handler=on_min,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="len",
        top_left=Vector2(450, 500),
        on_click_handler=on_len,
        font_size=30,
        color="Black"
    ),
    TextButton(
        text="is_empty",
        top_left=Vector2(620, 400),
        on_click_handler=on_is_empty,
        font_size=30,
        color="Black"
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
            for button in text_buttons:
                if event.button == pg.BUTTON_LEFT and button.is_hover():
                    button.click()

    screen.fill("White")
    screen.blit(sky_surface, sky_rectangle)

    # Horizontal line separating the visualization section and the manipulation section
    pg.draw.line(screen, "Black", Vector2(0, SCREEN_SIZE.y / 2), Vector2(SCREEN_SIZE.x, SCREEN_SIZE.y / 2), 2)

    for text_input in text_inputs:
        if text_input.has_focus():
            exists_focused_input = True
            focused_input = text_input

        text_input.render(screen)

    if not exists_focused_input:
        focused_input = None

    for button in text_buttons:
        button.render(screen)

    for label in labels:
        label.render(screen)

    pg.display.flip()
    clock.tick(MAX_FPS)
