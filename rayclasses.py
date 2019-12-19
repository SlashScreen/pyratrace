#rayclasses.py

#from vectors import Point, Vector
from functools import reduce
import math
import numpy as np

class Ray :
    def __init__(self,pos,dir):
        self.pos = pos
        self.dir = dir
        #print(dir)


def color(ray):
    if ray.dir.to_list() == [0,0,0]:
        d = ray.dir.to_list()
    else:
        d = ray.dir.unit().to_list()
    
    unitDirection = Vector(d[0],d[1],d[2])
    #print(unitDirection)
    t = .5*(unitDirection.y+1)
    return (Vector(1,1,1)*(t))+(Vector(.5, .7, 1)*(1-t))
    
class Vector:
        """
        A generic 3-element vector. All of the methods should be self-explanatory.
        """

        def __init__(self, x=0, y=0, z=0):
                self.x = x
                self.y = y
                self.z = z

        def norm(self):
                return math.sqrt(sum(num * num for num in self))

        def unit(self):
                """Return a Vector instance of the unit vector"""
                return Vector(
                    (self.x / self.magnitude()),
                    (self.y / self.magnitude()),
                    (self.z / self.magnitude())
                )

        def magnitude(self):
                """Return magnitude of the vector."""
                return math.sqrt(
                    reduce(lambda x, y: x + y, [x ** 2 for x in self.to_list()])
                )

        def to_list(self):
                '''Returns an array of [x,y,z] of the end points'''
                return [self.x, self.y, self.z]

        def normalize(self):
                return self / self.norm()

        def reflect(self, other):
                other = other.normalize()
                return self - 2 * (self * other) * other

        def __str__(self):
                return "Vector({}, {}, {})".format(*self)

        def __add__(self, other):
                return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

        def __sub__(self, other):
                return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

        def __mul__(self, other):
                if isinstance(other, Vector):
                        return self.x * other.x + self.y * other.y + self.z * other.z;
                else:
                        return Vector(self.x * other, self.y * other, self.z * other)

        def __rmul__(self, other):
                return self.__mul__(other)

        def __truediv__(self, other):
                return Vector(self.x / other, self.y / other, self.z / other)

        def __pow__(self, exp):
                if exp != 2:
                        raise ValueError("Exponent can only be two")
                else:
                        return self * self

        def __iter__(self):
                yield self.x
                yield self.y
                yield self.z
