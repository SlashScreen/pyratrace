#raytrace.py

from PIL import Image
from vectors import Point, Vector
from rayclasses import *

#define window, create image. img is the output, debug is the red and green 
window = {"w":200,"h":100}
img = Image.new("RGB",(window["w"],window["h"]))
raw = img.load()
debug = Image.new("RGB",(window["w"],window["h"]))
debugRaw = debug.load()
#define vectors needed
lowerLeftCorner = Vector((window['w']/100)*-1,(window['h']/100)*-1,-1)
hAxis = Vector((window['w']/50),0,0)
vAxis = Vector(0,(window['h']/50),0)
Origin = Vector(0,0,0)
#temporarily hardcoded spheres
hittableList = [Sphere(Vector(0,0,-1),.5),Sphere(Vector(2,-1,-2),.5),Sphere(Vector(-2,0,-2),.5)]
#loop through all screen pixels
for x in range(window["w"]):
    for y in range(window["h"]):
        #calculate UVs
        u = (x/window["w"])
        v = (y/window["h"])
        #build ray
        ray = Ray(Origin,.5*(lowerLeftCorner+(hAxis*(u))+(vAxis*v)).unit())
        
        #get pixel color
        col = color(ray,hittableList)
        #turn color into something readable by PIL (255-base tuple)
        o = (col*255).to_list()
        o = [int(x) for x in o]
        if u == v:
            d = (255,255,255)
        elif int((ray.dir.x/hAxis.x)*100) % int((5/window['w'])*100) == 0 or int((ray.dir.y/vAxis.y)*100) % int((5/window['h'])*100) == 0:
            d = (0,0,255)
        else:
            d = (int(abs(u*255)),int(abs(v*255)),int(.2*255))
        #set px color
        raw[x,y] = tuple(o)
        debugRaw[x,y] = d

img.show()
debug.show()
