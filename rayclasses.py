#rayclasses.py

###INCLUDES###

from functools import reduce
import math
import numpy as np
import random

###FUNCTIONS###

def color(ray,hittable): #Main render function: grabs color according to vector.
    # go through Hittable list
    for b in hittable:
        h,rec = b.hit(ray)
        if h > 0:
            target = rec.p + rec.n + randomInUnitSphere()
            return .5 * color(Ray(rec.p,target-rec.p),hittable)
        
    #Render sky - lerp from blue to white based on vertical ray position.
    d = ray.dir.to_list() 
    unitDirection = Vector(d[0],d[1],d[2]) #construct unit
    t = .5*(unitDirection.y+1) #lerp alpha value, based on how far down the vector is
    return (Vector(1,1,1)*(t))+(Vector(.5, .7, 1)*(1-t)) #take white, the base color, and then add blue (2nd vec) based on alpha value 

def random():
    random.seed()
    return random.random()

def randomInUnitSphere():
    p = Vector()
    while p.magnitude() >= 1:
        p = .2*(random(),random(),random()) - Vector(1,1,1)
    return p
        

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
            return -1,None
        else:
            t=(-b - math.sqrt(disc) / 2*a)
            p=ray.pointAtParameter(t)
            return (-b - math.sqrt(disc) / 2*a),hitRecord(t,p,(p-self.origin)/self.radius)
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
            return np.dot(np.array(self.to_list()),np.array(other.to_list()))

            
        def __pow__(self, exp):
                if exp != 2:
                        raise ValueError("Exponent can only be two")
                else:
                        return self * self

        def __iter__(self):
                yield self.x
                yield self.y
                yield self.z

class Camera:
    def __init__(self,lowerLeftCorner,hAxis,vAxis,samples,origin = Vector()):
        self.lowerLeftCorner = lowerLeftCorner
        self.hAxis = hAxis
        self.vAxis = vAxis
        self.origin = origin
        self.samples = samples
        self.aa = False #make this settable

    def move(self,diff): #move camera by some amount. diff is vector
        self.origin += diff

    def set(self,newLocation): #set camera to new position. newLocation is vector
        self.origin = newLocation

    def calculateRay(self,u,v):
        return Ray(self.origin,(self.lowerLeftCorner+(self.hAxis*u)+(self.vAxis*v)).unit())

    def cast(self,u,v,hitList,window): #ominous
        if self.aa:
            col = Vector()
            xSize = 1/window['w']
            ySize = 1/window['h']
            for s in range(self.samples):
                random.seed()
                col += color(self.calculateRay(u+random.uniform(-xSize,xSize),v+random.uniform(-ySize,ySize)),hitList)
            col = col / self.samples
            return col
        else:
            return color(self.calculateRay(u,v),hitList)
