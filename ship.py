import tkinter as tk
from plasma_ball import PlasmaBall
from hitbox import Hitbox
from ship_piece import ShipPiece
from PIL import Image, ImageTk, ImageOps
import math
import time

class Ship:
    def __init__(self, game, canvas, sprites_dir, x, y, ang):
        self.sprites_dir = sprites_dir
        self.color = sprites_dir[0]
        self.current_sprite = 0
        self.canvas = canvas
        self.p_lst = []
        self.sp_lst = []
        self.game = game
        self.ang = ang # ángulo inicial en sexagesimal
        self.prev_ang = ang
        self.current_rot = 0
        self.v = 3 # multiplicador de velocidad de la nave
        self.rot_v = 3
        self.r_filter = False
        # Sprite inicial -> 0
        self.set_sprite(0)

        # Cargar tkimg al canvas y guardar el objeto de canvas que lo representa
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

        self.cooldown = 0.8
        self.i_t = 0

        self.hitbox = Hitbox(self.canvas, self, "ship")
        self.p_maxtime = 3
        self.lives = 5
        self.active = True


    def set_sprite(self, sprite_num, flip=False):
        self.img = Image.open(f"{self.sprites_dir}/{self.color}_ship{sprite_num}.png")
        if flip: self.img = ImageOps.mirror(self.img)
        if self.r_filter: 
            self.apply_red_filter()
        self.tkimg = ImageTk.PhotoImage(self.img.rotate(self.get_img_ang()))

    def get_img_ang(self):
        return (360 - self.ang) - 90

    def get_position(self):
        return tuple(self.canvas.coords(self.el))
    
    def move(self, x, y):
        self.canvas.move(self.el, x, y)
    
    def move_forward(self):
        rads_ang = math.radians(self.ang)
        xshift = math.cos(rads_ang) * self.v
        yshift = math.sin(rads_ang) * self.v
        self.move(xshift, yshift)
    
    def check_outofbounds(self):
        w = self.game.width
        h = self.game.height
        x, y = self.get_position()
        if x > w + 16: self.canvas.move(self.el, -w - 32, 0)
        elif x < -16: self.canvas.move(self.el, w + 32, 0)
        if y > h + 16: self.canvas.move(self.el, 0, -h - 32)
        elif y < -16: self.canvas.move(self.el, 0, h + 32)
    
    def rotate_ah(self, *args): # rotar en antihorario
        self.prev_ang = self.ang
        self.ang -= self.rot_v
        self.ang %= 360
        self.current_rot = 0
    
    def rotate_h(self, *args): # rotar en sentido horario
        self.prev_ang = self.ang
        self.ang += self.rot_v
        self.ang %= 360
        self.current_rot = 1
    
    def delete(self): # eliminar la nave
        self.canvas.delete(self.el)
    
    def update(self):
        if self.active:
            self.move_forward() # Mover hacia adelante
            self.update_sprite() # Actualizar el sprite
            self.check_outofbounds()
            self.hitbox.update()
        for p in self.p_lst:
            p.update()
        if self.p_lst:
            t = self.p_lst[0].check_lifetime()
            if t >= self.p_maxtime:
                self.p_lst[0].desintegrate()
                self.p_lst.pop(0)
        if self.sp_lst:
            for piece in self.sp_lst:
                piece.update_angle()
                piece.move_forward()
    
    def update_sprite(self):
        # rotar mismo sprite
        self.animate_sprite()

        
        x, y = self.get_position()
        self.delete()
        self.el = self.canvas.create_image(x, y, image=self.tkimg)

    def animate_sprite(self):
        # Determinar si la nave está girando:
        # Si esta girando, utilizar los sprites de giro
        self.current_sprite = (self.current_sprite + 1) % 3 # Actualizar sprite
        if self.prev_ang == self.ang:
            self.set_sprite(self.current_sprite)
        else:
            if self.current_rot:
                self.set_sprite(self.current_sprite + 3) # Sprites de rotación [3 - 5]
            else:
                self.set_sprite(self.current_sprite + 3, flip=True) # Espejo
        # Actualizar el ángulo anterior
        self.prev_ang = self.ang

    def shoot(self, *args):
        self.actual_t = time.time()
        if self.actual_t - self.i_t >= self.cooldown:
            self.i_t = time.time()
            x, y = self.get_position()
            rads_ang = math.radians(self.ang)
            x += math.cos(rads_ang) * 16
            y += math.sin(rads_ang) * 16
            self.p_lst.append(PlasmaBall(self.game, self.canvas, self.ang, self.color, x, y))

    def hit(self, ang):
        self.lives -= 1
        #self.r_filter = True
        #self.game.after(200, self.deac_r_filter)

    def deac_r_filter(self):
        self.r_filter = False

    def apply_red_filter(self):
        width, height = self.img.size

        pixels = self.img.load()

        for py in range(height):
            for px in range(width):
                r, g, b, a = self.img.getpixel((px,py))
                newr = r
                newg = 0
                newb = 0
                newa = a
                pixels[px, py] = (newr, newg, newb, newa)
            
    def destroy(self, ang):
        
        x, y = self.get_position()
        self.delete()
        self.sp_lst.append(ShipPiece(self.game, self.canvas, ang + 30, self.sprites_dir, 1, x, y))
        self.sp_lst.append(ShipPiece(self.game, self.canvas, ang, self.sprites_dir, 2, x, y))
        self.sp_lst.append(ShipPiece(self.game, self.canvas, ang - 30, self.sprites_dir, 3, x, y))
        self.active = False
        self.game.after(1000, self.delete_pieces)

    def delete_pieces(self):
        for piece in self.sp_lst:
            piece.destroy()

        self.sp_lst = []
        
