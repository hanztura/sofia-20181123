import sys

import pyglet

from models import ImageTiling

# CONFIG
SCREEN_LENGTH = 640
IMAGE_FILENAME = 'image.png'
NUMBER_OF_REPETITIONS = sys.argv[1]

# check if number of repititions is valid
while True:
    try:
        NUMBER_OF_REPETITIONS = int(NUMBER_OF_REPETITIONS)
    except Exception as e:
        NUMBER_OF_REPETITIONS = 0
    finally:
        if NUMBER_OF_REPETITIONS < 1:
            message = 'Argument provided is not valid.'
            print(message)

            message = 'Enter a valid number of repititions>>> '
            NUMBER_OF_REPETITIONS = input(message)
        else:
            break

window = pyglet.window.Window(width=SCREEN_LENGTH, height=SCREEN_LENGTH)
base_image_length = SCREEN_LENGTH
last_image_length = 0
last_center = 0
tiling_iterations = []  # tiling objects

# loop through tiling iterations
for i in range(NUMBER_OF_REPETITIONS):
    length = last_image_length
    if length <= 0:
        length = base_image_length

    # create ImageTiling object
    tiling = ImageTiling(length=length, last_center=last_center)
    tiling_iterations.append(tiling)

    # update variables
    last_image_length = tiling.image_size
    last_center = tiling.center


@window.event
def on_draw():
    window.clear()

    for tiling in tiling_iterations:
        doge = pyglet.image.load(IMAGE_FILENAME)
        image_size = tiling.image_size
        doge.width = image_size
        doge.height = image_size

        q1_coordinate = tiling.quadrant_upper_left_coordinates
        q2_coordinate = tiling.quadrant_lower_left_coordinates
        q3_coordinate = tiling.quadrant_lower_right_coordinates

        # print doge image
        doge.blit(q1_coordinate[0], q1_coordinate[1])
        doge.blit(q2_coordinate[0], q2_coordinate[1])
        doge.blit(q3_coordinate[0], q3_coordinate[1])

    import pprint
    pprint.pprint(dir(doge))


pyglet.app.run()
