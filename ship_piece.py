import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import math
import random
import time

class ShipPiece:
    def __init__(self, game, canvas, ang, sprites_dir, piece, x, y):
        self.ang = ang
        self.canvas = canvas
        self.game = game
        self.sprites_dir = sprites_dir
        self.color = self.sprites_dir[0]
        self.v = random.randint(5, 10)
        self.ang_v = random.randint(10, 70)
        self.img_ang = (360 - self.ang) - 90
        self.t_i = time.time()
        self.img = Image.open(f"{self.sprites_dir}/{self.color}_piece{piece}.png")
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.img_ang))
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

        self.explode_img = Image.open(f"{self.sprites_dir}/{self.color}_explode.png")
        self.explode_tkimg = ImageTk.PhotoImage(self.explode_img.rotate(self.img_ang))
        self.fire_img = Image.open(f"{self.sprites_dir}/{self.color}_fire.png")
        self.fire_tkimg = ImageTk.PhotoImage(self.fire_img.rotate(180))
        self.fire = self.canvas.create_image(-100, -100, image=self.fire_tkimg)
    
    def destroy(self):
        x, y = self.get_position()
        self.delete()
        self.el = self.canvas.create_image(x, y, image=self.explode_tkimg)
        self.game.after(500, self.delete)

    def delete(self):
        self.canvas.delete(self.el)
    
    def get_position(self):
        return tuple(self.canvas.coords(self.el))
    
    def move_forward(self):
        rads_ang = math.radians(self.ang)
        x = math.cos(rads_ang) * self.v
        y = math.sin(rads_ang) * self.v
        self.move(x, y)
        self.update_trail()
    
    def update_trail(self):
        actual_t = time.time()
        if actual_t - self.t_i >= 0.05:
            self.canvas.delete(self.fire)
            x, y = self.get_position()
            self.fire = self.canvas.create_image(x-3, y-3, image=self.fire_tkimg)
            self.t_i = time.time()

    def move(self, x, y):
        self.canvas.move(self.el, x, y)

    def update_angle(self):
        # rotar mismo sprite
        self.img_ang = (self.img_ang + self.ang_v) % 360
        x, y = self.get_position()
        self.delete()
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.img_ang))
        self.el = self.canvas.create_image(x, y, image=self.tkimg)