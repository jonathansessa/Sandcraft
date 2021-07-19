import abc
import math

from .grid_object import GridObject
from .solid_body_particle import SolidBodyParticle


class SolidBody(GridObject):
    def __init__(
            self,
            id_color_dict,
            id_2d_list,
            width, height,
            col, row,
            vel_x, vel_y,
            acc_x, acc_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state):

        super().__init__(
            col, row,
            vel_x, vel_y,
            acc_x, acc_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state)

        self._id_color_dict = id_color_dict
        self._id_2d_list = id_2d_list
        self._width = width
        self._height = height
        self._particles = [[None for _ in range(width)] for _ in range(height)]

        c_width = int(math.floor(width * 0.5))
        c_height = int(math.floor(height * 0.5))

        self._col -= c_width
        self._row -= c_height

        for y in range(len(id_2d_list)):
            for x in range(len(id_2d_list[y])):
                curr_color = id_color_dict[id_2d_list[y][x]]
                if curr_color is None:
                    self._particles[y][x] = None
                else:
                    self._particles[y][x] = SolidBodyParticle(
                        self._col + x, self._row + y,
                        self._vel_x, self._vel_y,
                        self._acc_x, self._acc_y,
                        self._temp, self._temp_freeze, self._temp_boil,
                        self._density,
                        curr_color,
                        self._name,
                        self._flammability,
                        self._state)

    @abc.abstractmethod
    def clone(self, col, row):
        pass

    def emplace(self, driver):
        can_add = True

        for row in range(self._height):
            for col in range(self._width):
                if self._particles[row][col] is not None:
                    pos = (self._col + col, self._row + row)
                    if not driver.grid.is_in_bounds(pos) or driver.grid.exists(pos):
                        can_add = False

        if can_add:
            driver.add_solid_body(self)
            for row in range(self._height):
                for col in range(self._width):
                    if self._particles[row][col] is not None:
                        driver.add(self._particles[row][col])

    @abc.abstractmethod
    def update_on_tick(self, driver, grid):
        pass

    def contains(self, particle):
        for row in range(self._height):
            if particle in self._particles[row]:
                return True
        return False

    def empty(self):
        return len(self._particles) == 0
