from random import choice as random_choice
from pyglet import image as pyglet_image
from pyglet.sprite import Sprite


class ImageTiling(object):
    def __init__(self, *args, **kwargs):
        self.length = kwargs.get('length')
        self.last_center = kwargs.get('last_center', 0)

    @property
    def height(self):
        return self.length

    @property
    def width(self):
        return self.length

    @property
    def image_size(self):
        length = self.length
        size = length // 2
        return size

    @property
    def center(self):
        last_center = self.last_center
        image_size = self.image_size
        center = image_size + last_center
        return center

    @property
    def quadrant_upper_left_coordinates(self):
        """
        Returns a tuple.
        """
        last_center = self.last_center
        coordinates = (last_center, last_center)
        return coordinates

    @property
    def quadrant_lower_left_coordinates(self):
        """
        Returns a tuple.
        """
        last_center = self.last_center
        center = self.center
        coordinates = (center, last_center)
        return coordinates

    @property
    def quadrant_lower_right_coordinates(self):
        """
        Reverse of the lower left quadrant.

        Returns a tuple.
        """
        qllc = self.quadrant_lower_left_coordinates
        coordinates = (qllc[1], qllc[0])
        return coordinates


class Bubble(object):
    """docstring for Bubble"""
    DEFAULT_BUBBLES = (
        'bubble--red.png',
        'bubble--blue.png',
        'bubble--yellow.png'
    )
    DEFAULT_DIRECTIONS = (
        ('W', 'E'),
        ('N', 'S')
    )
    IMAGE_SIZE = 100
    bubble, possible_directions, current_direction = '', [], ''
    directions = []

    def __init__(self, *arg, **kwargs):
        super(Bubble, self).__init__()
        self.bubbles = kwargs.get('bubbles', self.DEFAULT_BUBBLES)
        self.directions = kwargs.get('directions', self.DEFAULT_DIRECTIONS)
        self.start_coordinates = kwargs.get('coordinates', (0, 0))
        self.move_counter = 0

        # initiate other variables
        self.set_start_coordinates()
        bubble_image = self.get_random_bubble()
        bubble_image = pyglet_image.load(bubble_image)
        self.bubble = Sprite(bubble_image)
        self.possible_directions = self.get_random_directions()

        x = self.start_coordinates[0]
        y = self.start_coordinates[1]
        width = kwargs.get('window_width')
        height = kwargs.get('window_height')

        # check if center x is beyond limits
        if x + self.IMAGE_SIZE > width:
            x = width - self.IMAGE_SIZE - 1
        elif x - self.IMAGE_SIZE < 0:
            x = 1

        # check if center y is beyond limits
        if y + self.IMAGE_SIZE > height:
            y = height - self.IMAGE_SIZE - 1
        elif y - self.IMAGE_SIZE < 0:
            y = 1

        self.bubble.position = (x, y)

    def should_bounce(self, width, height):
        should_bounce = False
        bubble = self.bubble
        center = self.get_center()
        center_x, center_y = center[0], center[1]
        image_size = self.IMAGE_SIZE // 2

        # check x if within boundary
        if center_x + image_size >= width:
            should_bounce = True
        elif center_x - image_size <= 0:
            should_bounce = True
        elif center_y + image_size >= height:
            should_bounce = True
        elif center_y - image_size <= 0:
            should_bounce = True

        return should_bounce

    def move(self, interval=1 / 60, **kwargs):
        self.set_current_direction(kwargs.get('window_width'), kwargs.get('window_height'))
        bubble = self.bubble
        current_direction = self.current_direction

        if current_direction == 'W':
            bubble.x -= 100 * interval
        elif current_direction == 'E':
            bubble.x += 100 * interval
        elif current_direction == 'N':
            bubble.y += 100 * interval
        elif current_direction == 'S':
            bubble.y -= 100 * interval

        self.move_counter += 1

    def bounce(self, directions, current_direction):
        # filter directions so it will remove the current direction
        directions = [d for d in directions if d != current_direction]

        new_direction = random_choice(directions)
        self.current_direction = new_direction

    def get_random_bubble(self):
        bubbles = self.bubbles
        bubble = random_choice(bubbles)
        return bubble

    def get_vertical_or_horizontal(self):
        directions = self.directions
        v_or_h = random_choice(directions)
        return v_or_h

    def get_random_directions(self):
        directions = self.directions
        directions = random_choice(directions)
        return directions

    def get_random_dir(self):
        possible_directions = self.possible_directions
        direction = random_choice(possible_directions)
        return direction

    def set_current_direction(self, width, height):
        possible_directions = self.possible_directions

        if not self.current_direction:
            # if no current direction set
            direction = random_choice(possible_directions)
            self.current_direction = direction
        else:
            # check if should bounce
            if self.should_bounce(width, height):
                self.bounce(possible_directions, self.current_direction)

    def set_start_coordinates(self):
        start_coordinates = self.start_coordinates
        image_size = self.IMAGE_SIZE // 2
        x = start_coordinates[0] - image_size
        y = start_coordinates[1] - image_size
        self.start_coordinates = (x, y)

    def get_center(self):
        bubble = self.bubble
        position = bubble.position
        x, y = position[0], position[1]
        image_size = self.IMAGE_SIZE // 2
        x += image_size
        y += image_size
        return (x, y)

    def blit(self, x=0, y=0):
        bubble = self.bubble
        bubble.blit(x, y)

    def draw(self):
        bubble = self.bubble
        bubble.draw()
