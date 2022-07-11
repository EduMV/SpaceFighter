import tkinter as tk
import math
from PIL import Image, ImageTk
import time


class PlasmaBall:
    def __init__(self, game, canvas, ang, color, x, y):
        self.ang = ang
        self.color = color
        self.canvas = canvas
        self.game = game
        self.img_ang = (360 - self.ang) - 90
        self.v = 10
        self.i_t = time.time()
        self.img = Image.open(f"{self.color}_pball_sprites/{self.color}_pball{0}.png")
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.img_ang))
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

        # l
        self.desint_img = Image.open(f"{self.color}_pball_sprites/{self.color}_dissapear.png")
        self.desint_tkimg = ImageTk.PhotoImage(self.desint_img.rotate(self.img_ang))
        self.impact_img = Image.open(f"{self.color}_pball_sprites/{self.color}_impact.png")
        self.impact_tkimg = ImageTk.PhotoImage(self.impact_img.rotate(self.img_ang))
    
    def check_outofbounds(self):
        w = self.game.width
        h = self.game.height
        x, y = self.get_position()
        if x > w + 16: self.canvas.move(self.el, -w - 32, 0)
        elif x < -16: self.canvas.move(self.el, w + 32, 0)
        if y > h + 16: self.canvas.move(self.el, 0, -h - 32)
        elif y < -16: self.canvas.move(self.el, 0, h + 32)
    
    def get_position(self):
        return tuple(self.canvas.coords(self.el))

    def move(self, x, y):
        self.canvas.move(self.el, x, y)

    def move_forward(self):
        rads_ang = math.radians(self.ang)
        x = math.cos(rads_ang) * self.v
        y = math.sin(rads_ang) * self.v
        self.move(x, y)
    
    def check_lifetime(self):
        actual_t = time.time()
        return actual_t - self.i_t

    def update(self):
        self.move_forward()
        self.check_outofbounds()

    def desintegrate(self):
        x, y = self.get_position()
        self.delete()
        self.el = self.canvas.create_image(x, y, image=self.desint_tkimg)
        self.game.after(500, self.delete)

    def impact(self):
        x, y = self.get_position()
        rads_ang = math.radians(self.ang)
        x += math.cos(rads_ang) * 10
        y += math.sin(rads_ang) * 10
        self.delete()
        self.el = self.canvas.create_image(x, y, image=self.impact_tkimg)
        self.game.after(300, self.delete)

    def delete(self):
        self.canvas.delete(self.el)
