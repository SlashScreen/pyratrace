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
    def pointAtParameter(self,t):
        return self.pos + (self.dir*t)

def hitSphere(origin,r,ray):
    oc = ray.pos-origin
    a = (ray.dir .dot( ray.dir))
    b = 2 * (oc.dot(ray.dir))
    c = (oc.dot(oc)) - (r*r)
    disc = b*b-4*a*c
    if disc < 0:
        return -1
    else:
        return (-b - math.sqrt(disc) / 2*a)
    #it's the quadratic formula. if the discriminant (4ac) is -, it yields an
    #imaginary number- which means it does not hit the sphere.


def color(ray):
    h = hitSphere(Vector(0,0,-1),.5,ray)
    if h > 0:
        N = (ray.pointAtParameter(h) - Vector(0,0,-1)).unit()
        return .5*Vector(N.x+1,N.y+1,N.z+1)
    if ray.dir.to_list() == [0,0,0]: #If it is 0,0,0, doing unit operation will not work, so just pass it 0.
        d = ray.dir.to_list() #because if unit worked (it doesn't- 0,0,0 makes it divide by 0) it would still be this.
    else:
        d = ray.dir.unit().to_list() #if it's not 0, then make a unit thing.
    
    unitDirection = Vector(d[0],d[1],d[2]) #construct unit
    t = .5*(unitDirection.y+1) #lerp alpha value, based on how far down the vector is
    return (Vector(1,1,1)*(t))+(Vector(.5, .7, 1)*(1-t)) #take white, the base color, and then add blue (2nd vec) based on alpha value 
    
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

        def dot(self, other):
            return self.magnitude() * other.magnitude() * ((self*other)/(self.magnitude()*other.magnitude()))

            
        def __pow__(self, exp):
                if exp != 2:
                        raise ValueError("Exponent can only be two")
                else:
                        return self * self

        def __iter__(self):
                yield self.x
                yield self.y
                yield self.z
