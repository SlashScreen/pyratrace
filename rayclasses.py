#rayclasses.py

from vectors import Point, Vector
from functools import reduce
import math

class Ray :
    def __init__(self,pos,dir):
        self.pos = pos
        self.dir = dir


def color(ray):
    if ray.dir.to_list() == [0,0,0]:
        d = ray.dir.to_list()
    else:
        d = ray.dir.unit().to_list()
    
    unitDirection = Vector(d[0],d[1],d[2])
    #print(unitDirection)
    t = .5*(unitDirection.y+1)
    return Vector(1,1,1).multiply(1-t).cross(Vector(.5, .7, 1))
    
class Vector(Vector): #class extension because a few things needed a tune up
    def unit(self):
        """Return a Vector instance of the unit vector"""
        return Vector(
            (self.x / self.magnitude()),
            (self.y / self.magnitude()),
            (self.z / self.magnitude())
        )
    def to_list(self):
        """Returns an array of [x,y,z] of the end points"""
        return [self.x, self.y, self.z]
    def magnitude(self):
        """Return magnitude of the vector."""
        return math.sqrt(
            reduce(lambda x, y: x + y, [x ** 2 for x in self.to_list()])
        )
