import tkinter as tk
import math

class Ship:
    angles = [3*math.pi/2, 5*math.pi/3, 11*math.pi/6] + [i* math.pi/6 for i in range(9)]

    def __init__(self, canvas, sprites_dir, x, y):
        self.color = sprites_dir[0]
        self.canvas = canvas
        self.img = tk.PhotoImage(file=sprites_dir + f"/{self.color}_ship0.png")
        self.el = self.canvas.create_image(x, y, image=self.img)
        
        self.sprites_lst = [
            tk.PhotoImage(file=sprites_dir + f"/{self.color}_ship{i}.png") for i in range(12)]
        
        self.ang = 3 * math.pi/2
        self.v = 3

    def get_position(self):
        return tuple(self.canvas.coords(self.el))
    
    def move(self, x, y):
        self.canvas.move(self.el, x, y)
    
    def move_forward(self):
        x = math.cos(self.ang) * self.v
        y = math.sin(self.ang) * self.v
        self.move(x, y)
    
    def rotate_ah(self, *args):
        if self.ang > 0:
            self.ang -= math.pi/64
        else:
            self.ang = 2 * math.pi - math.pi/64
    
    def rotate_h(self, *args):
        if self.ang < 2 * math.pi:
            self.ang += math.pi/64
        else:
            self.ang = 0 + math.pi/64
    
    def delete(self):
        self.canvas.delete(self.el)
    
    def update(self):
        self.move_forward()
        self.update_sprite()
    
    def update_sprite(self):
        min_val = 4
        for i in range(len(self.angles)):
            val = abs(self.ang-self.angles[i])
            if val < min_val:
                min_val = val
                min_index = i

        self.canvas.itemconfig(self.el,image=self.sprites_lst[min_index])
        

            
