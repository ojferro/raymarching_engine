#!/usr/bin/python3

from tkinter import *
import time
import math

debug = True


def debug_print(string):
    if debug:
        print(string)


class Shape():
    def __init__(self, x, y, r, colour=None):
        self.x = x
        self.y = y
        self.colour = colour


class Circle(Shape):
    def __init__(self, x, y, r, colour=None):
        super().__init__(x, y, colour)
        self.r = r
    def signed_dist(self, cam_pos):
        dist_vec = Vector((self.x, self.y)) - cam_pos
        return dist_vec.length() - self.r


# class Arithmetic():
# Helper class that will do vector math


class Vector():

    def __init__(self, pt=(0, 0)):
        self.x = pt[0]
        self.y = pt[1]

    def __sub__(self, v2):
        return Vector((v2.x-self.x, v2.y-self.y))

    def elementwise_add(self, v2):
        return Vector((self.x+v2.x, self.y+v2.y))

    def __add__(self, v2):
        return Vector((v2.x+self.x, v2.y+self.y))

    def scalar_mult(self, d):
        return Vector((self.x*d, self.y*d))

    def elementwise_mult(self, v2):
        return Vector((self.x*v2.x, self.y*v2.y))

    # def vector_from_pts(self, v1, v2):
    #     return Vector((pt2[0]-pt1[0], pt2[1]-pt2[1]))

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        self.x /= self.length()
        self.y /= self.length()


class Raymarcher():

    scene = []

    camera_position = Vector((80, 60))
    camera_rotation = 0 #TODO: Account for camera rotation
    image_plane_dist = 1
    # Cannot increase clipping plane for now. Must normalize color values first
    clipping_plane = 99

    epsilon = 0.1  # Dist < epsilon will be considered a collision

    pixel_dimensions = 4
    MAX_ITER_PER_PX = 2

    # a = Arithmetic()

    def __init__(self, master, width=200, height=100):
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.canvas = Canvas(master, width=width, height=height)
        self.canvas.pack()

    def draw_point(self, pt):
        self.canvas.create_line(pt[0], pt[1], pt[0]+1, pt[1])

    def draw_point_2D_world(self, x, color='gray50'):
        ''' Entire height of the screen is filled'''
        self.canvas.create_line(x, 0, x, self.CANVAS_HEIGHT, fill=color)

    def get_distance_to_scene(self):
        distances = []  # easier to parallelise
        for shape in self.scene:
            distances.append(shape.signed_dist(self.camera_position))
        return min(distances)

    def move_cam_in_dir(self, tmp_cam_pos, direction, step_size):
        if direction.length()-1 > 0.0001:
            direction.normalize()

        return tmp_cam_pos+direction.scalar_mult(step_size)

    def raymarch(self, debugger=None):
        if debugger:
            debugger.draw_point(self.camera_position, color='red')

        for x in range(0, self.CANVAS_WIDTH):
            debug_print("pixel {}".format(x))
            tmp_cam_pos = self.camera_position
            step_size = self.get_distance_to_scene()
            flag = False
            iteration_count = 0
            while step_size > self.epsilon and (tmp_cam_pos.x-self.camera_position.x) < self.clipping_plane \
                and iteration_count < self.MAX_ITER_PER_PX:
                iteration_count +=1
                debug_print("iterating {}, {}".format(
                    tmp_cam_pos.x, step_size))

                if not flag:
                    direction = self.camera_position - \
                        Vector(((x-self.CANVAS_WIDTH)*self.pixel_dimensions, self.image_plane_dist))
                    direction.normalize()
                    flag = True

                step_size = self.get_distance_to_scene()

                debug_print("STEP_SIZE {}".format(step_size))
                debug_print("DIRECTION {}, {}".format(direction.x, direction.y))
                debug_print("PREV_POS {}, {}".format(tmp_cam_pos.x, tmp_cam_pos.y))

                tmp_cam_pos = self.move_cam_in_dir(tmp_cam_pos, direction, step_size)

                debug_print("CURR_POS {}, {}".format(direction.x, direction.y))

                if debugger:
                    debugger.draw_line(tmp_cam_pos, self.camera_position)
                    # debugger.draw_circle(tmp_cam_pos, step_size)

            print("done px {}, {}, {}".format(x, tmp_cam_pos.x,  tmp_cam_pos.y))
            distance = tmp_cam_pos-self.camera_position
            distance = distance.length()
            # colors go from gray1=black to gray99=white.
            self.draw_point_2D_world(x, color='gray{}'.format(
                str(min(int(self.clipping_plane-distance), 99))))


class SceneDebugger():

    ''' Top down view of scene to help debug'''
    def __init__(self, master, width=100, height=100):
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.canvas = Canvas(master, width=width, height=height)
        self.canvas.pack()

    def draw_scene(self, scene):
        for shape in scene:
            if type(shape).__name__ == 'Circle':
                # TODO: Boundary checks
                self.canvas.create_oval(shape.x-shape.r, shape.y-shape.r, shape.x+shape.r, shape.y+shape.r)
    def draw_circle(self, pt, r):
        self.canvas.create_oval(pt.x-r, pt.y-r, pt.x+r, pt.y+r)

    def draw_point(self, v, color='black'):
        self.canvas.create_line(v.x, v.y, v.x+1, v.y, fill=color)

    def draw_line(self, v1, v2):
        self.canvas.create_line(v1.x, v1.y, v2.x, v2.y)


master = Tk()
rm = Raymarcher(master)

master2 = Tk()
sdb = SceneDebugger(master2)

################################################

# Define a scene
'''
Scene: 100 by 100
Top down view:
O = circle
c = camera

  clipping_plane
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

rm.scene.append(Circle(x=10, y=10, r=5))
rm.scene.append(Circle(x=50, y=30, r=10))
rm.scene.append(Circle(x=20, y=10, r=8))

sdb.draw_scene(rm.scene)
rm.raymarch(sdb)

print("Scene finished rendering")
master.mainloop()  # never exits
