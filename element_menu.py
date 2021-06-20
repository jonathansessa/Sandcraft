import particle

# For each type (particle, liquid, gas, solid)
# Make a label and list of menu buttons
# Draw
# Once done,
#

BUTTONS_PER_ROW = 10


class ElementMenu:
    def __init__(self, surface, x, y, width):
        self._surface = surface
        self._particles = particle.get_particles()
        self._x = x
        self._y = y
        self._width = width
        self._height = 0

    def contains(self, mouse_x, mouse_y):
        if mouse_x < self._x or self._x + self._width < mouse_x:
            return False

        if mouse_y < self._y or self._y + self._height < mouse_y:
            return False

        return True


class ElementSection:
    def __init__(self, surface, x, y, width, height, color):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._active = False
        self._enabled = True
        self._unlocked = True

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False

        if y < self._y or self._y + self._height < y:
            return False

        return True


class ElementButton:
    def __init__(self, surface, x, y, width, height, color):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color
        self._active = False
        self._enabled = True
        self._unlocked = True

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False

        if y < self._y or self._y + self._height < y:
            return False

        return True

