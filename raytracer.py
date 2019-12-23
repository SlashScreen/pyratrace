#raytrace.py

###INCLUDES###

from PIL import Image
from vectors import Point, Vector
from rayclasses import *

###VARIABLES###

#define window, create image. img is the output
window = {"w":200,"h":100}
img = Image.new("RGB",(window["w"],window["h"]))
raw = img.load()


#define vectors needed
lowerLeftCorner = Vector((window['w']/100)*-1,(window['h']/100)*-1,-1)
hAxis = Vector((window['w']/50),0,0) #I don't remmeber what H means. The x axis that the ray directio lerps across.
vAxis = Vector(0,(window['h']/50),0) #This is the y axis that it lerps across.
Origin = Vector(0,0,0) #camera position.

#define objects
#temporarily hardcoded spheres
hittableList = [Sphere(Vector(0,0,-1),.5),Sphere(Vector(2,-1,-2),.5),Sphere(Vector(-2,0,-2),.5)]
cam = Camera(lowerLeftCorner,hAxis,vAxis,3,Origin)
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
        col = cam.cast(u,v,hittableList,window)
        
        #turn color into something readable by PIL (255-base tuple)
        o = (col*255).to_list()
        o = [int(x) for x in o]
        
        #set px color
        raw[x,y] = tuple(o)

#Show result

img.show()
