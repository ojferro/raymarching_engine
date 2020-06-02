#!/usr/bin/python3

from tkinter import *
import time
import math


class Shape():
    def __init__(self, x, y, r, colour=None):
        self.x = x
        self.y = y
        self.colour = colour


class Circle(Shape):
    def __init__(self, x, y, r, colour=None):
        super().__init__(x, y, colour)
        self.r = r

    def signed_dist(self, cam_x, cam_y):
        return


class Point():
    def __init__(self, x, y, colour=None):
        self.x = x
        self.y = y
        self.colour = colour


class Vector():

    def __init__(self, pt=(0,0)):
        self.x = pt[0] 
        self.y = pt[1]

    def vector_from_pts(self, pt1, pt2):
        return Vector((pt2[0]-pt1[0], pt2[1]-pt2[1]))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        self.x /= self.length()
        self.y /= self.length()

class Raymarcher():

    scene = []
    camera_position = Point(0, 0)
    image_plane_dist = 1
    pixel_dimensions = 1/1000

    def __init__(self, master, width=200, height=100):
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.canvas = Canvas(master, width=width, height=height)
        self.canvas.pack()

    def draw_point(self, pt):
        self.canvas.create_line(pt[0], pt[1], pt[0]+1, pt[1])

    def get_distance_to_scene(self):
        distances = []  # easier to parallelise
        for shape in self.scene:
            distances.append(shape.signed_dist(self.camera_position))
        return min(distances)
    
    def raymarch(self):
        for x in range(0,self.CANVAS_WIDTH):
            for y in range(0, self.CANVAS_HEIGHT):
                direction = Vector(camera_position)

    # def march(self, direction)


master = Tk()

rm = Raymarcher(master)

################################################

# Define a scene
'''
Scene: 100 by 100
Top down view:
O = circle
c = camera (at (0,0))

 _______________
|               |
|          O    |
|               |
|    O          |
|               |
L_______c_______|
       / \
      /___\
    image_plane

y
|_x

'''

rm.scene.append(Circle(x=10, y=10, r=1))
rm.scene.append(Circle(x=10, y=100, r=1))
rm.scene.append(Circle(x=20, y=10, r=1))

rm.draw_point((50, 50))

print("Scene finished rendering")
master.mainloop()  # never exits
