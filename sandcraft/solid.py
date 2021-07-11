from .particle import Particle
from . import particle_data


class Solid(Particle):
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

    def clone(self, col, row):
        return Solid(
            col, row,
            self._vel_x, self._vel_y,
            self._acc_x, self._acc_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._name,
            self._flammability,
            self._state)

    def update_on_tick(self, driver, grid):
        if self._needs_update is False:
            return

        self._update_vel()

        pos_path = self._get_positions_in_path(grid)

        if len(pos_path) == 0:
            self._needs_update = False

        for next_pos in pos_path:
            pos = (self._col, self._row)

            if grid.exists(next_pos) is False:
                self._force_update_near(grid)
                grid.swap(pos, next_pos)
            else:
                collider = grid.get(next_pos)

                # Heat transfer
                near_list = grid.get_near((self._col, self._row))
                for particle in near_list:

                    temp_diff = (self._temp - particle.temp) / 50
                    if particle.name == "fire":
                        temp_diff = temp_diff * self._flammability
                    particle._update_temp(particle, particle.temp + temp_diff)
                    self._update_temp(self, self._temp - temp_diff)

                # Burning
                if (self.name == "powder" or self.name == "wood") and (self._temp_freeze <= self._temp):
                    oldtemp = self._temp
                    self._melt(driver, grid, particle_data.template_fire.clone(self._col, self._row))
                    self._update_temp(self, oldtemp)

                # Molten stone or sand -> lava
                if (self.name == "stone" or self.name == "sand") and self._temp_freeze <= self._temp:
                    oldtemp = self._temp
                    self._melt(driver, grid, particle_data.template_lava.clone(self._col, self._row))
                    self._update_temp(self, oldtemp)

                if self._density > collider.density:
                    self._force_update_near(grid)
                    grid.swap(pos, next_pos)
                else:
                    left_pos = (self._col - 1, self._row + 1)
                    right_pos = (self._col + 1, self._row + 1)

                    left_in_bounds = grid.is_in_bounds(left_pos)
                    right_in_bounds = grid.is_in_bounds(right_pos)

                    left_exists = left_in_bounds and grid.exists(left_pos)
                    right_exists = right_in_bounds and grid.exists(right_pos)

                    if left_exists is False and left_in_bounds \
                            or left_exists is True and self._density > grid.get(left_pos).density:
                        self._force_update_near(grid)

                        grid.swap(pos, left_pos)

                    elif right_exists is False and right_in_bounds \
                            or right_exists is True and self._density > grid.get(right_pos).density:
                        self._force_update_near(grid)

                        grid.swap(pos, right_pos)

                    else:
                        self._needs_update = False
                break
