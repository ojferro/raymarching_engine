from tkinter import *

CANVAS_WIDTH = 200
CANVAS_HEIGHT = 100

def draw_point(pt):
    c.create_line(pt.x, pt.y, pt.x+1, pt.y)

master = Tk()

c = Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
c.pack()

