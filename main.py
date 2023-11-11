import sys

import pygame as pg
from pygame import Vector2, Rect

from dialog import Dialog
from label import Label
from patient import PatientData, Patient
from priority_queue import AdaptablePriorityQueue
from text_button import TextButton
from text_input import TextInput


# Utility methods
def update_key_locator_dict():
    key_locator_dict.clear()
    for locator in pq.locators():
        key_locator_dict[locator.key] = locator
        key_locator_dict[locator.key].value.key = locator.key


def print_updates(tag: str = ""):
    if tag:
        print(f"{tag}: {pq}")
        print(f"{tag}: sequential - {pq.string_sequential()}")
        # print(f"{tag}: {key_locator_dict}")
    else:
        print(pq)
        print("sequential - " + pq.string_sequential())
        # print(key_locator_dict)


# Button callbacks
def remove_dialog():
    global is_dialog_showing
    is_dialog_showing = False


def show_dialog():
    global is_dialog_showing
    is_dialog_showing = True


def on_add():
    try:
        key = int(text_inputs[0].text)
        value = text_inputs[1].text

        key_locator_dict[key] = pq.add(key, PatientData(key, value))

        print_updates(tag="on_add")

        text_inputs[0].clear()
        text_inputs[1].clear()

    except ValueError as e:
        print(f"on_add: {e}")
        dialog.set_message("Key should be an integer")
        show_dialog()
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
            dialog.set_message("The queue is empty.")
            show_dialog()
            print(f"change_priority: The queue is empty!")

    except ValueError as e:
        print(f"change_priority: {e}")
        dialog.set_message("Key should be an integer")
        show_dialog()
        text_inputs[2].clear()
        text_inputs[3].clear()

    except KeyError as e:
        print(f"change_priority: {e}")
        dialog.set_message("There is no patient with the key given")
        show_dialog()
        text_inputs[2].clear()
        text_inputs[3].clear()


def on_remove():
    global is_dialog_showing
    try:
        if not pq.is_empty():
            key = int(text_inputs[4].text)
            _, value = pq.remove(key_locator_dict[key])
            update_key_locator_dict()
            print_updates(tag="on_remove")

            dialog.set_message(f"({value.key}, {value.name})")
            show_dialog()

            text_inputs[4].clear()
        else:
            dialog.set_message("There is no patient to remove!")
            show_dialog()
            text_inputs[4].clear()
            print("on_remove: There is nothing to remove!")

    except ValueError as e:
        print(f"on_remove: {e}")
        dialog.set_message("The key should be an integer!")
        show_dialog()
        text_inputs[4].clear()

    except KeyError as e:
        print(f"on_remove: {e}")
        dialog.set_message("There is no patient with the key given")
        show_dialog()
        text_inputs[4].clear()


def on_remove_min():
    if not pq.is_empty():
        key, value, _ = pq.remove_min()
        update_key_locator_dict()
        print_updates(tag="on_remove_min")

        dialog.set_message(f"({key}, {value.name})")
        show_dialog()
    else:
        print("on_remove_min: There is nothing to remove!")
        dialog.set_message("There is nothing to remove!")
        show_dialog()


def on_min():
    if not pq.is_empty():
        minimum = key_locator_dict[pq.min()[0]].value
        dialog.set_message(f"({minimum.key}, {minimum.name})")
        show_dialog()
        print(f"min={key_locator_dict[pq.min()[0]]}")
    else:
        dialog.set_message("The queue is empty.")
        show_dialog()
        print("min: The queue is empty!")


def on_len():
    dialog.set_message(f"len = {len(pq)}")
    show_dialog()
    print(f"len={len(pq)}")


def on_is_empty():
    dialog.set_message(f"is_empty = {pq.is_empty()}")
    show_dialog()
    print(f"is_empty={pq.is_empty()}")


# pygame-specific setup
pg.init()
pg.display.set_caption("hospital-queue-visualization")
SCREEN_SIZE = Vector2(800, 600)
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()
MAX_FPS = 60

# Background setup
GROUND_HEIGHT = SCREEN_SIZE.y / 2
sky_surface = pg.image.load("./assets/graphics/sky.png")
sky_rectangle = sky_surface.get_rect()
sky_rectangle.topleft = Vector2(0, 0)

# TextInput setup
KEY_TEXT_INPUT_SIZE = Vector2(50, 30)
VALUE_TEXT_INPUT_SIZE = Vector2(100, 30)
text_inputs = [
    TextInput(top_left=Vector2(50, 400), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(120, 400), size=VALUE_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(50, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),
    TextInput(top_left=Vector2(120, 450), size=KEY_TEXT_INPUT_SIZE, font_size=30),

    TextInput(top_left=Vector2(120, 500), size=KEY_TEXT_INPUT_SIZE, font_size=30),
]
focused_input: TextInput | None = None
exists_focused_input = False

# Label setup
label_text_list = ["key", "value", "key", "new key", "key", "value"]
labels = []
for i in range(len(text_inputs)):
    rect = Rect(Vector2(0, 0), Vector2(text_inputs[i].size))
    rect.topleft = text_inputs[i].input_rectangle.bottomleft
    labels.append(Label(label_text_list[i], rect))

# Data structure setup
key_locator_dict: dict[int, AdaptablePriorityQueue.Locator] = dict()
pq = AdaptablePriorityQueue()

# Dialog setup
dialog = Dialog(SCREEN_SIZE, on_dismiss=remove_dialog)
is_dialog_showing = False

# TextButton setup
text_buttons = [
    TextButton(text="Add", top_left=Vector2(250, 400), on_click_handler=on_add, font_size=30, color="Black"),
    TextButton(text="Change priority", top_left=Vector2(250, 450), on_click_handler=on_update, font_size=30,
               color="Black"),
    TextButton(text="Remove", top_left=Vector2(250, 500), on_click_handler=on_remove, font_size=30, color="Black"),
    TextButton(text="Remove min", top_left=Vector2(450, 400), on_click_handler=on_remove_min, font_size=30,
               color="Black"),
    TextButton(text="Min", top_left=Vector2(450, 450), on_click_handler=on_min, font_size=30, color="Black"),
    TextButton(text="len", top_left=Vector2(450, 500), on_click_handler=on_len, font_size=30, color="Black"),
    TextButton(text="is_empty", top_left=Vector2(620, 400), on_click_handler=on_is_empty, font_size=30, color="Black")
]

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if focused_input is not None:
                focused_input.update_text(event.key, event.unicode)

        if event.type == pg.MOUSEBUTTONUP:
            if is_dialog_showing:
                if dialog.dismiss_button.is_hover():
                    dialog.click_dismissed_button()
            else:
                for button in text_buttons:
                    if event.button == pg.BUTTON_LEFT and button.is_hover():
                        button.click()

    screen.fill("White")
    screen.blit(sky_surface, sky_rectangle)

    # Horizontal line separating the visualization section and the manipulation section
    pg.draw.line(screen, "Black", Vector2(0, GROUND_HEIGHT), Vector2(SCREEN_SIZE.x, GROUND_HEIGHT), 2)

    i = 0
    for _, patient_data, _ in pq:
        Patient(patient_data, Vector2(200 + i * 120, GROUND_HEIGHT)).render(screen)
        i += 1

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

    if is_dialog_showing and dialog is not None:
        dialog.render(screen)

    pg.display.flip()
    clock.tick(MAX_FPS)
