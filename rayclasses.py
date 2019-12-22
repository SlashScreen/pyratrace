#rayclasses.py

###INCLUDES###

from functools import reduce
import math
import numpy as np

###FUNCTIONS###

def color(ray,hittable): #Main render function: grabs color according to vector.
    # go through Hittable list
    for b in hittable:
        h = b.hit(ray)
        if h > 0:
            N = (ray.pointAtParameter(h) - Vector(0,0,-1)).unit() #calculate normal, athough im pretty sure this is wrong haha
            return .5*Vector(N.x+1,N.y+1,N.z+1)
        
    #Render sky - lerp from blue to white based on vertical ray position.
    d = ray.dir.to_list() 
    unitDirection = Vector(d[0],d[1],d[2]) #construct unit
    t = .5*(unitDirection.y+1) #lerp alpha value, based on how far down the vector is
    return (Vector(1,1,1)*(t))+(Vector(.5, .7, 1)*(1-t)) #take white, the base color, and then add blue (2nd vec) based on alpha value 
    

###CLASSES###

class Material: #this is unused right now
    def __init__(self,alb,diff,met,trans,sub,lum,shader = None, tex = None):
        self.albedo = alb
        self.diffuse = diff
        self.shiny = met #I am totally blanking on  the technical term for this. Specular?...
        self.transparency = trans #trans rights fuck jk rowling
        self.subsurface = sub
        self.luminosity = lum
        self.tex = tex #There are a lot of textures models these days need. will probably have to be an object with normals, distortion, etc. packed in
        self.shader = shader #NTS: when this object is hit apply shader to that pixel

        #General flow is:
        #Get pos hit on mesh, pull pixel color from uv map at that point, then blend with color gained from  shadows, reflections, etc.

class Mesh: #unused right now
    def __init__(self):
        self.mesh = None

class Sphere: #Sphere object.
    def __init__(self,origin,r,mat = None):
        self.origin = origin
        self.radius = r
        self.material = mat #mat watson?? from super mega???
        
    def hit(self,ray): #Does ray collide with sphere
        #see if and where ray hits sphere and if it does what normal
        oc = ray.pos-self.origin
        a = (ray.dir .dot( ray.dir))
        b = 2 * (oc.dot(ray.dir))
        c = (oc.dot(oc)) - (self.radius**2)
        disc = b**2-4*a*c
        if disc < 0:
            return -1
        else:
            return (-b - math.sqrt(disc) / 2*a)
        #it's the quadratic formula. if the discriminant (4ac) is -, it yields an
        #imaginary number- which means it has no roots, and thus does not hit the sphere.


class hitRecord: #unused temporarily.
    def __init__(self,t,p,normal):
        self.n = normal
        self.p = p
        self.t = t

class Ray: #Ray.
    def __init__(self,pos,dir):
        self.pos = pos
        self.dir = dir
        
    def pointAtParameter(self,t): #gets point t along the ray, and returns it in world space.
        return self.pos + (self.dir*t)


class Vector: #vector class, has all methods. Comprised from several people's vector methods as well as my own.
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
                m = self.magnitude()
                if m == 0:
                    return Vector (0,0,0)
                else:
                    return Vector(
                        (self.x / m),
                        (self.y / m),
                        (self.z / m)
                    )

        def magnitude(self):
                """Return magnitude of the vector."""
                return math.sqrt(
                    reduce(lambda x, y: x + y, [x ** 2 for x in self.to_list()])
                )

        def to_list(self):
                '''Returns an array of [x,y,z] of the end points'''
                return [self.x, self.y, self.z]

        def normalize(self): #yes this also means unit. I didn't know that.
                return self / self.norm()

        def reflect(self, other):
                other = other.normalize()
                return self - 2 * (self * other) * other

        def __str__(self):
                return "Vector({}, {}, {})".format(*self)

        def __add__(self, other):
                if isinstance(other, Vector):
                    return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
                else:
                    return Vector(self.x + other, self.y + other, self.z + other)

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

        def dot(self, other): #is this wrong?
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
