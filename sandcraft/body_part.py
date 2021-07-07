from .grid import Grid
from .body import Body
from .particle import Particle
from . import particle_data

class BodyPart(Particle):
    def __init__(
            self,
            col, row,
            vel_x, vel_y, #should only be allowed to move at velocity of 1
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state):
        super().__init__(
            col, row,
            vel_x, vel_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state)
        self._body = None


    def clone(self, col, row):
        return BodyPart(
            col, row,
            self._vel_x, self._vel_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._name,
            self._flammability,
            self._state)

    """
        "update_on_tick" is needed for every particle due to the way 
    """

    def update_on_tick(self, driver, grid):
        #if self._needs_update is False:
        #    return
        self._body.updateBody(driver, grid)
        return

    """
        Latch rules. 
            1. If part is placed with no adjacent nodes, create new body.
            2. If part is placed next to a preexisting body, add it to said body.
            3. If part is placed next to a "dropped" body, create new body and add said particle to it.
    """
    def latch(self, grid): #particle will attempt to "latch" or add itself to a nearby body
        
        near_list = grid.get_near((self.col, self.row))
        latched = False

        for particle in near_list:
            if isinstance(particle, BodyPart):
                if particle._body is not None: #Maybe rule 2
                        latched = particle._body.addPart(self, grid)
        
        if not latched: #rule 1 and 3
            self._body = Body()
            self._body.addPart(self, grid)


    """
        As of now, canDown will return:
            False:
                1. if next pos is out of bounds.
                2. if next pos is occupied.
            True:
                1. if next pos in empty.
            In the future, occupation will take into account density.

    """
    def canDown(self, grid): #can the particle move down? Is the below space in bounds and empty?
        next_x = self.col + self._vel_x
        next_y = self.row + self._vel_y
        next_pos = (next_x, next_y)
        if grid.is_in_bounds(next_pos) is False:
            return False
        elif grid.exists(next_pos):
            return False

        return True
    
    def changeColor(self): #wanted to use this to visualize what particles were added to ._bottomLayer
            self._color = (0, 75, 0)
    
    """
        def moveDown(self, driver, grid):
            next_x = self._col + self._vel_x
            next_y = self._row + self._vel_y
            next_pos = (next_x, next_y)
            pos = (self._col, self._row)
            if grid.is_in_bounds(next_pos):
                grid.swap(pos, next_pos)

    """