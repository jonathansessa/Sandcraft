from sandcraft.particle import Particle
from sandcraft import particle_data
from random import *


class Fixed(Particle):
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
        return Fixed(
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
        if self.name == "Water Generator":
            if not grid.exists((self.col + 1, self.row)):
                driver.add(particle_data.template_water.clone(self.col + 1, self.row))

        if self.name == "bush":
            growth = random()
            if growth < 0.003 and self.row > 6:
                if not grid.exists((self.col, self.row - 1)):
                    driver.add(particle_data.template_bush.clone(self.col, self.row - 1))
            growth = random()
            if growth < 0.001:
                if not grid.exists((self.col + 1, self.row)):
                    driver.add(particle_data.template_bush.clone(self.col + 1, self.row))
            growth = random()
            if growth < 0.001:
                if not grid.exists((self.col - 1, self.row)):
                    driver.add(particle_data.template_bush.clone(self.col - 1, self.row))

        if self.name == "vine":
            growth = random()
            if growth < 0.03 and self.row > 6:
                if not grid.exists((self.col, self.row - 1)):
                    driver.add(particle_data.template_vine.clone(self.col, self.row - 1))
            growth = random()
            if growth < 0.001 and self.row % 7 == 0:
                if not grid.exists((self.col + 1, self.row)):
                    driver.add(particle_data.template_vine.clone(self.col + 1, self.row))
            growth = random()
            if growth < 0.001 and self.row % 7 == 0:
                if not grid.exists((self.col - 1, self.row)):
                    driver.add(particle_data.template_vine.clone(self.col - 1, self.row))

        if self._needs_update is False:
            return

        near_list = grid.get_near((self._col, self._row))

        # Heat transfer
        for particle in near_list:
            temp_diff = (self._temp - particle.temp) / 50
            particle.update_temp(particle.temp + temp_diff)
            self.update_temp(self._temp - temp_diff)

        # All fixed solids above boil temp -> gas
        if self._temp_boil <= self._temp:
            self.boil(driver, grid, particle_data.template_steam.clone(self._col, self._row))

        # Ice melts into water
        if self.name == "ice" and self._temp_freeze <= self._temp:
            oldtemp = self._temp
            self.melt(driver, grid, particle_data.template_water.clone(self._col, self._row))
            self.update_temp(oldtemp)

        # Basalt and metal melts into lava
        if (self.name == "basalt" or self.name == "metal") and self._temp_freeze <= self._temp:
            oldtemp = self._temp
            self.melt(driver, grid, particle_data.template_lava.clone(self._col, self._row))
            self.update_temp(oldtemp)

        # Wood burns
        if self.name == "wood" and self._temp_freeze <= self._temp:
            oldtemp = self._temp
            self.melt(driver, grid, particle_data.template_fire.clone(self._col, self._row))
            self.update_temp(oldtemp)

        # Molten metal -> lava
        if self.name == "metal" and self._temp_freeze <= self._temp:
            oldtemp = self._temp
            self.melt(driver, grid, particle_data.template_lava.clone(self._col, self._row))
            self.update_temp(oldtemp)

        self._needs_update = False
