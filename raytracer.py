#raytrace.py

###INCLUDES###

from PIL import Image
from vectors import Point, Vector
from rayclasses import *

###VARIABLES###

#define window, create image. img is the output, debug is the red and green 
window = {"w":200,"h":100}
img = Image.new("RGB",(window["w"],window["h"]))
raw = img.load()
debug = Image.new("RGB",(window["w"],window["h"]))
debugRaw = debug.load()

#define vectors needed
lowerLeftCorner = Vector((window['w']/100)*-1,(window['h']/100)*-1,-1)
hAxis = Vector((window['w']/50),0,0) #I don't remmeber what H means. The x axis that the ray directio lerps across.
vAxis = Vector(0,(window['h']/50),0) #This is the y axis that it lerps across.
Origin = Vector(0,0,0) #camera position.

#temporarily hardcoded spheres
hittableList = [Sphere(Vector(0,0,-1),.5),Sphere(Vector(2,-1,-2),.5),Sphere(Vector(-2,0,-2),.5)]

###RENDER LOOP##

#loop through all screen pixels. x goes left-right and y goes up-down.
for x in range(window["w"]):
    for y in range(window["h"]):
        
        #calculate UVs
        u = (x/window["w"])
        v = (y/window["h"])
        
        #build ray
        #With my debugging trials, I can deduce that the problem *might be* with this line here.
        #what its doing is taking the left corner, and then moving the ray by how much it has gone left and down.
        ray = Ray(Origin,(lowerLeftCorner+(hAxis*u)+(vAxis*v)).unit())
        
        #get pixel color
        col = color(ray,hittableList)
        
        #turn color into something readable by PIL (255-base tuple)
        o = (col*255).to_list()
        o = [int(x) for x in o]
        
        #Gen Debug image
        #Ok yes,  the debug image looks like a hot mess, I know.
        #How to read it:
        #Colors are your basic UV "hello World".
        #The white line is to see if the u and v are iterating linearly. if it is straight, they are.
        #The horrble blue thing is, if there is no distortion in the image, a grid of uniform thickness.
        #however, you will  see that it is not. It is, instead, pinched at the middle.
        #Here, we can see that the problem is the vector, and not, in fact, the UVs.
        if u == v: 
            d = (255,255,255) #draw white line
        elif int((ray.dir.x/hAxis.x)*100) % int((5/window['w'])*100) == 0 or int((ray.dir.y/vAxis.y)*100) % int((5/window['h'])*100) == 0:
            d = (0,0,255) #Draw blue grid
        else: #draw hello world
            d = (int(abs(u*255)),int(abs(v*255)),int(.2*255))
            
        #set px color
        raw[x,y] = tuple(o)
        debugRaw[x,y] = d

#Show result

img.show()
debug.show()
