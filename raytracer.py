#raytrace.py

from PIL import Image
#from vectors import Point, Vector
from rayclasses import *

window = {"w":200,"h":100}
img = Image.new("RGB",(window["w"],window["h"]))
raw = img.load()
lowerLeftCorner = Vector(-2,-1,-1)
hAxis = Vector(4.0,0,0)
vAxis = Vector(0,2,0)
Origin = Point(0,0,0)
for x in range(window["w"]-1):
    for y in range(window["h"]-1):
        u = (x/window["w"])
        v = (y/window["h"])
        #print(u)
        ray = Ray(Origin,lowerLeftCorner .sum( hAxis.multiply(u).sum( vAxis.multiply(v))))
        col = color(ray)
        o = col.multiply(255).to_list()
        o = [int(x) for x in o]
        raw[x,y] = tuple(o)

img.show()
