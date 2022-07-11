import tkinter as tk
from ship import Ship

class SpaceFighter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.title("Space Fighter")
        self.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self, bg="#003b59", width=self.width, height=self.height)
        self.canvas.pack()
        self.s1 = Ship(self, self.canvas, "w_ship_sprites", 100, 500, 270)
        self.s2 = Ship(self, self.canvas, "b_ship_sprites", 700, 100, 90)
        self.pressed = {}
        self.bindings_init()
        self.game_loop()

    def bindings_init(self):
        # movimiento
        for key in ["a", "d", "j", "l", "c", "m"]:
            self.bind(f"<KeyPress-{key}>", self.key_pressed)
            self.bind(f"<KeyRelease-{key}>", self.key_released)
            self.pressed[key] = False

    def key_pressed(self, event):
        self.pressed[event.keysym] = True

    def key_released(self, event):
        self.pressed[event.keysym] = False
    
    def check_presses(self):
        if self.pressed["a"]: self.s1.rotate_ah()
        if self.pressed["d"]: self.s1.rotate_h()
        if self.pressed["j"]: self.s2.rotate_ah()
        if self.pressed["l"]: self.s2.rotate_h()
        if self.pressed["c"]: self.s1.shoot()
        if self.pressed["m"]: self.s2.shoot()
        self.canvas.update()
    
    def check_ship_colisions(self):
        for i in range(len(self.s1.p_lst)):
            x, y = self.s1.p_lst[i].get_position()
            if self.s2.hitbox.collision_point(x, y):
                ang = self.s1.p_lst[i].ang
                self.s1.p_lst[i].impact()
                self.s1.p_lst.pop(i)
                self.s2.hit(ang)
                break
            
        for i in range(len(self.s2.p_lst)):
            x, y = self.s2.p_lst[i].get_position()
            if self.s1.hitbox.collision_point(x, y):
                ang = self.s2.p_lst[i].ang
                self.s2.p_lst[i].impact()
                self.s2.p_lst.pop(i)
                self.s1.hit(ang)
                break

    def check_colisions(self):
        self.check_ship_colisions()

    def game_loop(self):
        self.check_presses()
        self.s1.update()
        self.s2.update()
        self.check_colisions()
        self.after(50, self.game_loop)

if __name__ == "__main__":
    sf = SpaceFighter()
    sf.mainloop()
