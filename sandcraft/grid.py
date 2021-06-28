from .config import *
from .particle import Particle


"""
    px_to_cell converts pixel coordinates into column or row coordinates, depending on whether you
    pass an x or a y value.
    This is useful in cases such as converting the mouse's x and y positions to their respective column and row
    counterparts in the grid.
"""
def px_to_cell(px):
    return int(px / PARTICLE_SIZE)


class Grid:
    def __init__(self):
        self.__num_cols = int(WINDOW_WIDTH / PARTICLE_SIZE)
        self.__num_rows = int(WINDOW_HEIGHT / PARTICLE_SIZE)
        self.__left = int(MARGIN / PARTICLE_SIZE)
        self.__right = int((MARGIN + SANDBOX_WIDTH) / PARTICLE_SIZE)
        self.__top = int((MARGIN * 2) / PARTICLE_SIZE)
        self.__bottom = int((MARGIN * 2 + SANDBOX_HEIGHT) / PARTICLE_SIZE)
        self.__cells = [[None for col in range(self.__num_cols)] for row in range(self.__num_rows)]

    """
        emplace adds a particle to its column and row, replacing the particle currently in that position.
        
        WARNING: This should not be used to add particles into the grid. Rather, the Driver's add method should be used,
        which calls emplace. If not, particles will not be added, updated, and rendered properly.
    """
    def emplace(self, particle):
        self.__cells[particle.row][particle.col] = particle

    def remove(self, particle):
        self.__cells[particle.row][particle.col] = None

    """
        swap switches the positions of two particles in the grid, also updating the positions of each particle.
        
        parameter lhs_pos is a tuple representing a column and row like so: (column, row)
        parameter rhs_pos is a tuple representing a column and row like so: (column, row)
    """
    def swap(self, lhs_pos, rhs_pos):
        lhs = self.__cells[lhs_pos[1]][lhs_pos[0]]
        rhs = self.__cells[rhs_pos[1]][rhs_pos[0]]

        self.__cells[lhs_pos[1]][lhs_pos[0]], self.__cells[rhs_pos[1]][rhs_pos[0]] = \
            self.__cells[rhs_pos[1]][rhs_pos[0]], self.__cells[lhs_pos[1]][lhs_pos[0]]

        if isinstance(lhs, Particle):
            lhs.set_pos(rhs_pos[0], rhs_pos[1])

        if isinstance(rhs, Particle):
            rhs.set_pos(lhs_pos[0], lhs_pos[1])

    """
        is_in_bounds returns whether a specified position is in bounds of the grid.
        
        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def is_in_bounds(self, pos):
        return self.__left <= pos[0] < self.__right and self.__top <= pos[1] < self.__bottom

    """
        exists returns whether there is a particle at the specified position.
        
        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def exists(self, pos):
        return self.__cells[pos[1]][pos[0]] is not None

    """
        is_in_bounds_and_exists combines the is_in_bounds and exists methods,
        returning whether the position is in bounds and there is a particle currently at the position.
        
        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def is_in_bounds_and_exists(self, pos):
        return self.is_in_bounds(pos) and self.exists(pos)

    """
        get returns the particle at the specified position, or None if there is no particle at the specified position.
        It is useful to check the is_in_bounds and exists methods to determine whether there is a particle at the
        position prior to calling the get method.
        
        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def get(self, pos):
        return self.__cells[pos[1]][pos[0]]

    """
        get_near returns the four particles around the particle at a specified position.
        the particles returned are to the:
            top,
            bottom,
            left,
            right
        of the specified position.

        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def get_near(self, pos):
        near_list = []
        col = pos[0]
        row = pos[1]

        self.__push_if_able(near_list, (col, row - 1))
        self.__push_if_able(near_list, (col, row + 1))
        self.__push_if_able(near_list, (col - 1, row))
        self.__push_if_able(near_list, (col + 1, row))

        return near_list

    """
        __push_if_able is a helper method for the get_near method that pushes the particle at the designated position
        to the specified list, if the position is in bounds and there is a particle there.

        parameter target_list is a list to which the particle currently at the designated position will be pushed,
            if the position is in bounds and there is currently a particle there.
        parameter pos is a tuple representing a column and row like so: (column, row)
    """
    def __push_if_able(self, target_list, pos):
        if self.is_in_bounds_and_exists(pos):
            target_list.append(self.get(pos))
