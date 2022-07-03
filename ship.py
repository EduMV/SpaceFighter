import tkinter as tk
from PIL import ImageTk
from PIL import Image
import math

class Ship:

    def __init__(self, canvas, sprites_dir, x, y, ang):
        self.color = sprites_dir[0]
        self.canvas = canvas

        self.ang = ang # ángulo inicial en sexagesimal
        self.v = 3 # multiplicador de velocidad de la nave

        self.img = Image.open(sprites_dir + f"/{self.color}_ship0.png") # Cargar imagen con pillow
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang())) # Rotar al angulo inicial

        # Cargar tkimg al canvas y guardar el "elemento"
        self.el = self.canvas.create_image(x, y, image=self.tkimg)
        
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
    
    def rotate_ah(self, *args):
        self.ang -= 3
        self.ang %= 360
    
    def rotate_h(self, *args):
        self.ang += 3
        self.ang %= 360
    
    def delete(self):
        self.canvas.delete(self.el)
    
    def update(self):
        self.move_forward()
        self.update_sprite()
    
    def update_sprite(self):
        x, y = self.get_position()
        self.delete()
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang()))
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

            
