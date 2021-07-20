import abc
import math


class GridObject(metaclass=abc.ABCMeta):
    def __init__(
            self,
            col, row,
            vel_x, vel_y,
            acc_x, acc_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state):

        self._col = col
        self._row = row
        self._vel_x = vel_x
        self._vel_y = vel_y
        self._acc_x = acc_x
        self._acc_y = acc_y
        self._temp = temp
        self._temp_freeze = temp_freeze
        self._temp_boil = temp_boil
        self._density = density
        self._color = color
        self._name = name
        self._flammability = flammability
        self._state = state

    @abc.abstractmethod
    def clone(self, col, row):
        pass

    @abc.abstractmethod
    def emplace(self, driver):
        pass

    """
        _true_vel_x returns the value that the col will be updated by every tick (conversion from float to int)
    """
    def _true_vel_x(self):
        return int(math.floor(self._vel_x))

    """
        _true_vel_y returns the value that the row will be updated by every tick (conversion from float to int)
    """
    def _true_vel_y(self):
        return int(math.floor(self._vel_y))

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row

    @property
    def temp(self):
        return self._temp

    @property
    def density(self):
        return self._density

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state
