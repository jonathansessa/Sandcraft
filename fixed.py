import liquid
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
            type,
            flammability,
            state):
        super().__init__(
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            type,
            flammability,
            state)

    def clone(self, col, row):
        return Fixed(
            col, row,
            self._vel_x, self._vel_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._type,
            self._flammability,
            self._state)

    def update_on_tick(self, driver, grid):
        if self._needs_update is False:
            return

        near_list = grid.get_near((self._col, self._row))

        # Heat transfer
        for particle in near_list:
            temp_diff = (self._temp - particle._temp) / 50
            particle._update_temp(particle, particle._temp + temp_diff)
            self._update_temp(self, self._temp - temp_diff)

        # All fixed solids above boil temp -> gas
        if self._temp_boil <= self._temp:
            self._boil(driver, grid, particle_data.template_steam.clone(self._col, self._row))

        # Ice melts into water
        if self.type == "ice" and self._temp_freeze <= self._temp:
            oldTemp = self._temp
            self._melt(driver, grid, particle_data.template_water.clone(self._col, self._row))
            self._update_temp(self, oldTemp)

        # Basalt and metal melts into lava
        if (self.type == "basalt" or self.type == "metal") and self._temp_freeze <= self._temp:
            oldTemp = self._temp
            self._melt(driver, grid, particle_data.template_lava.clone(self._col, self._row))
            self._update_temp(self, oldTemp)

        # Wood burns
        if self.type == "wood"  and self._temp_freeze <= self._temp:
            oldTemp = self._temp
            self._melt(driver, grid, particle_data.template_fire.clone(self._col, self._row))
            self._update_temp(self, oldTemp)

        # Molten metal -> lava
        if self._type == "metal" and self._temp_freeze <= self._temp:
            oldtemp = self._temp
            self._melt(driver, grid, particle_data.template_lava.clone(self._col, self._row))
            self._update_temp(self, oldtemp)


        self._needs_update = False
