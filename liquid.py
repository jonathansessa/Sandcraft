import random
from particle import Particle
import particle_data


class Liquid(Particle):
    def __init__(
            self,
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            type,
            flammability):
        super().__init__(
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            type,
            flammability)

    def clone(self, col, row):
        return Liquid(
            col, row,
            self._vel_x, self._vel_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._type,
            self._flammability)

    def update_on_tick(self, driver, grid):
        if self._needs_update is False:
            return

        pos = (self._col, self._row)

        next_x = self._col + self._vel_x
        next_y = self._row + self._vel_y
        next_pos = (next_x, next_y)

        if grid.is_in_bounds(next_pos):
            if grid.exists(next_pos) is False:
                self._force_update_near(grid)
                grid.swap(pos, next_pos)
            else:

                collider = grid.get(next_pos)

                near_list = grid.get_near((self._col, self._row))
                for particle in near_list:

                    temp_diff = (self._temp - particle._temp) / 50
                    particle._update_temp(particle, particle._temp + temp_diff)
                    self._update_temp(self, self._temp - temp_diff)

                if self._temp_boil <= self._temp:
                    self._boil(driver, grid, particle_data.template_steam.clone(self._col, self._row))

                if self._temp_freeze >= self._temp:
                    self._freeze(driver, grid, particle_data.template_basalt.clone(self._col, self._row))

                if self._density > collider.density:
                    self._force_update_near(grid)
                    grid.swap(pos, next_pos)
                else:
                    pos_left = (self._col - 1, self._row)
                    pos_right = (self._col + 1, self._row)

                    can_go_left = grid.is_in_bounds(pos_left)           \
                        and grid.exists(pos_left) is False              \
                        or grid.is_in_bounds(pos_left)                  \
                        and grid.exists(pos_left)                       \
                        and self._density > grid.get(pos_left).density

                    can_go_right = grid.is_in_bounds(pos_right)         \
                        and grid.exists(pos_right) is False             \
                        or grid.is_in_bounds(pos_right)                 \
                        and grid.exists(pos_right)                      \
                        and self._density > grid.get(pos_right).density

                    min_vel_x = -1 if can_go_left else 0
                    max_vel_x = 1 if can_go_right else 0

                    if min_vel_x == max_vel_x == 0:
                        self._needs_update = False
                    else:
                        vel_x = random.randrange(min_vel_x, max_vel_x + 1)
                        next_pos = (self._col + vel_x, self._row)

                        self._force_update_near(grid)
                        grid.swap(pos, next_pos)
        else:
            self._needs_update = False
