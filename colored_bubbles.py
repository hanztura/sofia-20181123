from pyglet import app as pyglet_app, clock
from pyglet.text import Label
from pyglet.window import (
    mouse, Window
)

from models import Bubble

window = Window()
bubbles = []
WINDOW_WIDTH, WINDOW_HEIGHT = window.width, window.height 


def update(dt):
    for bubble in bubbles:
        bubble.move(dt, window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT)


@window.event
def on_draw():
    window.clear()
    for bubble in bubbles:
        bubble.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        coordinates = (x, y)
        bubbles.append(Bubble(
            coordinates=coordinates,
            window_width=WINDOW_WIDTH,
            window_height=WINDOW_HEIGHT
        ))


clock.schedule_interval(update, 1 / 60)
pyglet_app.run()
