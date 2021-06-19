from particle import Particle
import particle_data


class Solid(Particle):
    def __init__(
            self,
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color):
        super().__init__(
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color)

    def clone(self, col, row):
        return Solid(
            col, row,
            self._vel_x, self._vel_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color)

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

                if self._temp_boil <= collider.temp:
                    self._boil(driver, grid, particle_data.template_steam.clone(self._col, self._row))
                elif self._density > collider.density:
                    self._force_update_near(grid)
                    grid.swap(pos, next_pos)
                else:
                    left_pos = (self._col - 1, self._row + self._vel_y)
                    right_pos = (self._col + 1, self._row + self._vel_y)

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
        else:
            self._needs_update = False
