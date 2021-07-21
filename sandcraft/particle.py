import abc
import pygame
from .config import PARTICLE_SIZE
from .grid_object import GridObject


class Particle(GridObject, metaclass=abc.ABCMeta):
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

    def emplace(self, driver):
        driver.add(self)

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

    def deny_update(self):
        self._needs_update = False

    """
        set_pos changes the particle's current col and row in the grid
    """
    def set_pos(self, col, row):
        self._col = col
        self._row = row

    """
        __boil is defined to reduce redundancy between the state classes (solid, liquid, gas, etc.)
        
        Freezing and melting are identical in function for now.
    """
    def boil(self, driver, grid, new_particle):
        self._is_live = False
        near_list = grid.get_near((self._col, self._row))
        for particle in near_list:
            particle.force_update()
        driver.add(new_particle)

    def freeze(self, driver, grid, new_particle):
        self._is_live = False
        near_list = grid.get_near((self._col, self._row))
        for particle in near_list:
            particle.force_update()
        driver.add(new_particle)

    def melt(self, driver, grid, new_particle):
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
        _update_vel updates the current velocity according to the acceleration.
    """
    def _update_vel(self):
        self._vel_x += self._acc_x
        self._vel_y += self._acc_y

    """
        _get_particles_in_path returns a list of particles that have possible collisions upon the next position update.
    """
    def _get_particles_in_path(self, grid):
        in_path = []

        positions_in_path_list = self._get_positions_in_path(grid)

        for pos in positions_in_path_list:
            if grid.exists(pos):
                in_path.append(grid.get(pos))

        return in_path

    """
        _get_positions_in_path returns a list of positions that have possible collisions upon the next position update.
    """
    def _get_positions_in_path(self, grid):
        in_path = []

        probe_x = self._col
        probe_y = self._row
        final_x = self._col + self._true_vel_x()
        final_y = self._row + self._true_vel_y()

        if final_x < grid.left:
            final_x = grid.left
        elif final_x >= grid.right:
            final_x = grid.right - 1

        if final_y < grid.top:
            final_y = grid.top
        elif final_y >= grid.bottom:
            final_y = grid.bottom - 1

        step_x = -1 if probe_x > final_x else 1
        step_y = -1 if probe_y > final_y else 1

        while probe_x != final_x or probe_y != final_y:
            if probe_x != final_x:
                probe_x += step_x

            if probe_y != final_y:
                probe_y += step_y

            in_path.append((probe_x, probe_y))

        return in_path

    """
        _update_temp changes the temperature of the particle, for collision purposes
    """
    def update_temp(self, new_temp):
        self._temp = new_temp

    """
        properties (read only)
    """

    @property
    def is_live(self):
        return self._is_live

    @property
    def needs_update(self):
        return self._needs_update
