import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import math

class Ship:
    def __init__(self, canvas, sprites_dir, x, y, ang):
        self.sprites_dir = sprites_dir
        self.color = sprites_dir[0]
        self.current_sprite = 0
        self.canvas = canvas

        self.ang = ang # ángulo inicial en sexagesimal
        self.prev_ang = ang
        self.current_rot = 0
        self.v = 3 # multiplicador de velocidad de la nave

        self.img = Image.open(sprites_dir + f"/{self.color}_ship0.png") # Cargar imagen con pillow
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang())) # Rotar al angulo inicial

        # Cargar tkimg al canvas y guardar el "elemento"
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

    def change_sprite(self, sprite_num, flip=False):
        self.img = Image.open(f"{self.sprites_dir}/{self.color}_ship{sprite_num}.png")
        if flip: self.img = ImageOps.mirror(self.img)
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang()))

    def get_img_ang(self):
        return (360 - self.ang) - 90

    def get_position(self):
        return tuple(self.canvas.coords(self.el))
    
    def move(self, x, y):
        self.canvas.move(self.el, x, y)
    
    def move_forward(self):
        rads_ang = math.radians(self.ang)
        x = math.cos(rads_ang) * self.v
        y = math.sin(rads_ang) * self.v
        self.move(x, y)
        if self.prev_ang == self.ang:
            self.current_sprite = (self.current_sprite + 1) % 3
            self.change_sprite(self.current_sprite)
        else:
            if self.current_rot:
                self.current_sprite = (self.current_sprite + 1) % 3
                self.change_sprite(self.current_sprite + 3)
            else:
                self.current_sprite = (self.current_sprite + 1) % 3
                self.change_sprite(self.current_sprite + 3, flip=True)

        self.prev_ang = self.ang
    
    def rotate_ah(self, *args):
        self.prev_ang = self.ang
        self.ang -= 3
        self.ang %= 360
        self.current_rot = 0
    
    def rotate_h(self, *args):
        self.prev_ang = self.ang
        self.ang += 3
        self.ang %= 360
        self.current_rot = 1
    
    def delete(self):
        self.canvas.delete(self.el)
    
    def update(self):
        self.move_forward() # Mover hacia adelante
        self.update_sprite() # Actualizar el sprite
    
    def update_sprite(self):
        x, y = self.get_position()
        self.delete()
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang()))
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

            
