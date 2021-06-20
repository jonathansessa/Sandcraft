COLOR_SAND = (255, 255, 0)
COLOR_WATER = (0, 191, 255)
COLOR_STEAM = (224, 224, 224)
COLOR_WOOD = (153, 76, 0)
COLOR_AIR = (0, 0, 0)


def get_particles():
    particles = {
        "Sand": COLOR_SAND,
        "Water": COLOR_WATER,
        "Steam": COLOR_STEAM,
        "Wood": COLOR_WOOD
    }
    return particles


def is_solid(pixel):
    if pixel == COLOR_SAND or pixel == COLOR_WOOD:
        return True
    else:
        return False


def is_liquid(pixel):
    if pixel == COLOR_WATER:
        return True
    else:
        return False


def is_gas(pixel):
    if pixel == COLOR_STEAM:
        return True
    else:
        return False


class Particle:
    def __init__(self, x, y, t):
        self._vx = 0
        self._vy = 0
        self._x = x
        self._y = y
        self._t = t

    def get_vx(self):
        return self._vx

    def set_vx(self, vx):
        self._vx = vx

    def get_vy(self):
        return self._vy

    def set_vy(self, vy):
        self._vy = vy

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_t(self):
        return self._t

    def set_t(self, t):
        self._t = t

    def update_vy(self, a):
        self._vy += a
        if self._vy > 10:
            self._vy = 10
        elif self._vy < -10:
            self._vy = -10

    def update_vx(self, a):
        self._vx += a
        if self._vx > 5:
            self._vx = 5
        elif self._vx < -5:
            self._vx = -5

    vx = property(get_vx, set_vx)
    vy = property(get_vy, set_vy)
    x = property(get_x, set_x)
    y = property(get_y, set_y)
    t = property(get_t, set_t)
