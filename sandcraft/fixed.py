from particle import Particle
import particle_data


class Fixed(Particle):
    def __init__(
            self,
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name):
        super().__init__(
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name)

    def clone(self, col, row):
        return Fixed(
            col, row,
            self._vel_x, self._vel_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._name)

    def update_on_tick(self, driver, grid):
        if self._needs_update is False:
            return

        near_list = grid.get_near((self._col, self._row))

        for particle in near_list:
            if self._temp_boil < particle.temp:
                self._boil(driver, grid, particle_data.template_steam.clone(self._col, self._row))
                break

        self._needs_update = False
