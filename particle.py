import abc
import pygame
from config import PARTICLE_SIZE


class Particle(metaclass=abc.ABCMeta):
    def __init__(
            self,
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color):

        self._col = col
        self._row = row
        self._vel_x = vel_x
        self._vel_y = vel_y
        self._temp = temp
        self._temp_freeze = temp_freeze
        self._temp_boil = temp_boil
        self._density = density
        self._color = color
        self._is_live = True
        self._needs_update = True

    """
        clone is an abstract method that is overridden by state classes deriving from Particle.
        This function returns a clone of the callee.
        This function is useful in cases such as the Painter class, which holds a template particle that
        is cloned to the mouse's current column and row in the grid when the left mouse button is pressed.
    """
    @abc.abstractmethod
    def clone(self, col, row):
        pass

    """
        update_on_tick is an abstract method that is overridden by state classes deriving from Particle.
        This is the function that handles the particle's movement and interactions.
    """
    @abc.abstractmethod
    def update_on_tick(self, driver, grid):
        pass

    """
        render draws the particle to the screen using a primitive pygame Rect
    """
    def render(self, screen):
        pygame.draw.rect(
            screen,
            self._color,
            pygame.Rect(
                self._col * PARTICLE_SIZE,
                self._row * PARTICLE_SIZE,
                PARTICLE_SIZE,
                PARTICLE_SIZE))

    """
        force_update will flip the particle's _needs_update boolean flag to True, which will result in the
        particle being updated the next tick.
        This is necessary, because particles will get stuck and/or not interact properly if their update
        flag is False, as it will never be reset.
        This method is generally called by other particles during their own update_on_tick cycles.
    """
    def force_update(self):
        self._needs_update = True

    """
        set_pos changes the particle's current col and row in the grid
    """
    def set_pos(self, col, row):
        self._col = col
        self._row = row

    """
        __boil is defined to reduce redundancy between the state classes (solid, liquid, gas, etc.)
    """
    def _boil(self, driver, grid, new_particle):
        self._is_live = False
        near_list = grid.get_near((self._col, self._row))
        for particle in near_list:
            particle.force_update()
        driver.add(new_particle)

    """
        __force_update_near is defined to reduce redundancy between the state classes (solid, liquid, gas, etc.)
    """
    def _force_update_near(self, grid):
        near_list = grid.get_near((self._col, self._row))
        for particle in near_list:
            particle.force_update()

    """
        properties (read only)
    """
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
    def is_live(self):
        return self._is_live

    @property
    def color(self):
        return self._color