import random
import pygame
from sandcraft.particle import Particle
from sandcraft import particle_data


class Gas(Particle):
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

        self._lifespan = pygame.time.get_ticks() + 3000
        self._remaining = 3000

    def clone(self, col, row):
        return Gas(
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
        if (pygame.time.get_ticks() > self._lifespan) or (self._temp <= self._temp_freeze):
            driver.delete(self)
            return

        if self._needs_update is False:
            return

        min_vel_x = -1 if grid.is_in_bounds((self._col - 1, self._row)) else 0
        max_vel_x = 1 if grid.is_in_bounds((self._col + 1, self._row)) else 0

        if min_vel_x == max_vel_x:
            self._vel_x = min_vel_x
        else:
            self._vel_x = random.randrange(min_vel_x, max_vel_x + 1)

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

                if self.name != "void" and collider.name == "void":
                    driver.delete(self)
                    break

                # Heat Transfer
                near_list = grid.get_near((self._col, self._row))
                for particle in near_list:
                    temp_diff = (self._temp - particle.temp) / 50
                    particle.update_temp(particle.temp + temp_diff)
                    self.update_temp(self._temp - temp_diff)

                    # Metal -> lava when heated by fire
                    if particle.name == "metal" and particle.temp_freeze <= particle.temp:
                        oldtemp = particle.temp
                        particle.melt(driver, grid, particle_data.template_lava.clone(particle.col, particle.row))
                        particle.update_temp(oldtemp)

                    # Burning
                    if (particle.name == "powder" or particle.name == "wood") and (
                            particle.temp_freeze <= particle.temp):
                        oldtemp = particle.temp
                        particle.melt(driver, grid, particle_data.template_fire.clone(particle.col, particle.row))
                        particle.update_temp(oldtemp)

                if self._density > collider.density:
                    self._force_update_near(grid)
                    grid.swap(pos, next_pos)

                else:
                    pos_left = (self._col - 1, self._row)
                    pos_right = (self._col + 1, self._row)

                    can_go_left = grid.is_in_bounds(pos_left) \
                                  and grid.exists(pos_left) is False \
                                  or grid.is_in_bounds(pos_left) \
                                  and grid.exists(pos_left) \
                                  and self._density > grid.get(pos_left).density

                    can_go_right = grid.is_in_bounds(pos_right) \
                                   and grid.exists(pos_right) is False \
                                   or grid.is_in_bounds(pos_right) \
                                   and grid.exists(pos_right) \
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
                break

    def save_lifespan(self):
        self._remaining = self._lifespan - pygame.time.get_ticks()

    def load_lifespan(self):
        self._lifespan = pygame.time.get_ticks() + self._remaining
