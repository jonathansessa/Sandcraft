from .body_part import *
from .grid import Grid
from .particle import Particle
from sandcraft import body_part

"""
    As of now, a body is where the calculations for physical interactions with other particles will occur
"""

class Body():
    def __init__(self):
        self._BodyParts = [] #all of the particles in this body
        self._dropped = True
        self._totalWeight = 0
        self._bottomLayer = [] #all the particles that make up the bottom of the body. Will take into account for particle interaction
        self._dropped = False
        self._needs_update = False
    """
        _dropped is an attribute that will let us know if the body has hit the maximum size. 
        Once the body has hit the maximum size, it is "dropped" and will actually start recieving physics
    """
    def isDropped(self):
        return self._dropped

    """
        addPart adds a bodyparticle to the body in question. If the body has more than 36 "BodyParts",
        then it will not be added and return false. 36 is an arbitrary number i came up with since you can easily get
        a body with 36 particles using the add tool at a brush size of 6. I just thought it was a good number to test with.
    """
    def addPart(self, part, grid): #adds part to BodyParts and sets part's body to Body, makes sure bottom particles are correct
        if self._dropped:#once body is dropped, you cannot add new particles
            return False

        self._BodyParts.append(part)
        part._body = self
        print("Added:",part.row,",",part.col)
        
        if len(self._BodyParts) >= 4:
            print("dropping...")
            #self.dropBody(grid)
        
        return True
        
    """
        dropBody is called once the body reaches maximums size. Each particle in the body is scanned.
        If the body particle has an empty space below it, it is added to the _bottomLayer list.
        The particles in _bottomLayer will be the only particles where physical interaction is taken into account (for now).

    """
    def dropBody(self, grid): #once body reaches a maximum size, physics are added to entire body
        self._dropped = True

        for part in self._BodyParts: #bottomLayer creation. decides what particles will physically interact
            print("col:",part._col)
            
            pos = (part._col, part._row)
            next_x = part._col + part._vel_x
            next_y = part._row + part._vel_y
            next_pos = (next_x, next_y)
            if not grid.exists(next_pos) and grid.is_in_bounds(next_pos):
                self._bottomLayer.append(part)
                print("Placed:",part.row,",",part.col)
            
            #if part.canDown(grid):
            #    self._bottomLayer.append(part)
            #    part.changeColor()
            #    print("bottomCol:",part._col)
            """
                #print("is in bounds:", grid.is_in_bounds(next_pos))
                #print("exists:", grid.exists(next_pos))
                #if isinstance(next_part, Particle):
                #    print("instance:", next_part._name)
                #else:
                #    print("instance: none")
                #print("instance:", next_part, Particle)
            """
            """
                        if isinstance(next_part, Particle):
                            if next_part._body is not None:
                                if next_part._body is not part._body:
                                    self._bottomLayer.append(part)

                if grid.is_in_bounds(next_pos) is False:
                    self._bottomLayer.append(part)
                else:
                    if grid.exists(next_pos):
                        if isinstance(grid.get(next_pos), Particle):
                            if grid.get(next_pos)._body is not None:
                                if grid.get(next_pos)._body is not part._body:
                                    self._bottomLayer.append(part)
                    else:
                        self._bottomLayer.append(part)
            """
        #self._needs_update = True
        print("Bottom Size:",len(self._bottomLayer))

    """
        #self._BodyParts.sort(key = lambda x: x._row) #organizes based on row, best this way if no y direction velocity
        print(len(self._bottomLayer))
        print(len(self._BodyParts))
        for part in self._BodyParts:
            print(part.col)
        for part in self._bottomLayer:
            print(part.col)
            part.changeColor()
    """

    """
        updateBody is my way of implimenting the "update_on_tick" function we have for all the particles.
        Basically if all the particles in the _bottomLayer can move down, all particles in the body move down as well.
        If one particle in _bottomLayer cannot "move down", then the entire body will stay in place.
    """
    def updateBody(self, driver, grid): #returns true if an update will occur
        #print("hit update")
        #if self._needs_update is False:
        #    return
        
        downer = True #keeps tabs if the body is going to move or not

        for part in self._bottomLayer: #checks bottom layer bodyparts if movement is possible
            
            pos = (part._col, part._row)
            next_x = part._col + part._vel_x
            next_y = part._row + part._vel_y
            next_pos = (next_x, next_y)

            if grid.exists(next_pos):#if theres a particle we cant update the body
                downer = False
                break
            if not grid.is_in_bounds(next_pos):#if its not in bounds we cant update the body
                downer = False
                break

        if downer:#body movement done here
            self.moveBodyDown(driver, grid)
            self._needs_update = True
        else:
            for part in self._BodyParts: #all particles updates set to false
                part._needs_update = False
            self._needs_update = False
        """
        if not collide: #moves down all particles if bottom layer does not collide
            for part in self._bottomLayer:
                #part.moveDown(driver, grid)
        else:
            self._needs_update = False
        """

    """
        moveBodyDown will update all the particles and move each down one space
    """
    def moveBodyDown(self, driver, grid):
        for part in self._BodyParts:
            pos = (part._col, part._row)
            next_x = part._col + part._vel_x
            next_y = part._row + part._vel_y
            next_pos = (next_x, next_y)
            grid.swap(pos, next_pos)
