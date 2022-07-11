import tkinter as tk
import math
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class Hitbox:
    ship_steps = [(3*(2**(1/2)), 45), (11, 0), (6, -90), (11, 180), (202**(1/2), -90 - math.degrees(math.atan2(9, 11))), (28, 90)]
    
    def __init__(self, canvas, obj, shape):
        self.canvas = canvas
        self.shape = shape
        self.obj = obj
        self.points_lst = []
        self.show_hitbox = False
        self.create_poly(self.shape)

    def create_poly(self, shape):
        if shape == "ship": steps = self.ship_steps

        x, y = self.obj.get_position()
        ang = self.obj.ang
        ang_rad = math.radians(ang)
        self.points_lst = []
        self.points_tuple_lst = []
        for step in steps:
            step_ang_rad = math.radians(step[1])
            x += step[0] * math.cos(ang_rad + step_ang_rad)
            y += step[0] * math.sin(ang_rad + step_ang_rad)
            self.points_lst.append(x)
            self.points_lst.append(y)
            self.points_tuple_lst.append((x, y))
        if self.show_hitbox:
            self.draw_poly()

    def draw_poly(self):
        self.el = self.canvas.create_polygon(*tuple(self.points_lst))
    
    def collision_point(self, x, y):
        return Polygon(self.points_tuple_lst).contains(Point(x, y))

    def update(self):
        if self.show_hitbox:
            self.canvas.delete(self.el)
        self.create_poly(self.shape)