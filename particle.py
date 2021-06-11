COLOR_SAND = (255, 255, 0)
COLOR_WATER = (0, 191, 255)
COLOR_WOOD = (153, 76, 0)
COLOR_AIR = (0, 0, 0)


def is_solid(pixel):
    if pixel == COLOR_SAND:
        return True
    else:
        return False


def is_liquid(pixel):
    if pixel == COLOR_WATER:
        return True
    else:
        return False


class Particle:
    def __init__(self):
        self._id = 0
        self._velocity = 0
        self._color = (255, 255, 255)
        self._has_been_updated = False
        self._x = 0
        self._y = 0

    def get_id(self):
        return self._id

    def get_color(self):
        return self._color

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    x = property(get_x, set_x)
    y = property(get_y, set_y)


class Sand(Particle):
    def __init__(self, x, y):
        super().__init__()
        self._id = 1
        self._velocity = 0
        self._color = (255, 255, 0)
        self._has_been_updated = False
        self._x = x
        self._y = y


class Water(Particle):
    def __init__(self, x, y):
        super().__init__()
        self._id = 2
        self._velocity = 0
        self._color = (0, 191, 255)
        self._has_been_updated = False
        self._x = x
        self._y = y
