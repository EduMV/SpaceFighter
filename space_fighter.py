import tkinter as tk
from ship import Ship

class SpaceFighter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.title("Jet Fighter")
        self.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self, bg="#003b59", width=self.width, height=self.height)
        self.canvas.pack()
        self.s1 = Ship(self.canvas, "w_ship_sprites", 100, 500, 270)
        self.s2 = Ship(self.canvas, "b_ship_sprites", 700, 100, 90)
        self.pressed = {}
        self.bindings_init()
        self.game_loop()

    def bindings_init(self):
        for key in ["Left", "Right", "a", "d"]:
            self.bind(f"<KeyPress-{key}>", self.key_pressed)
            self.bind(f"<KeyRelease-{key}>", self.key_released)
            self.pressed[key] = False

    def key_pressed(self, event):
        self.pressed[event.keysym] = True

    def key_released(self, event):
        self.pressed[event.keysym] = False
    
    def check_presses(self):
        if self.pressed["Left"]: self.s1.rotate_ah()
        if self.pressed["Right"]: self.s1.rotate_h()
        if self.pressed["a"]: self.s2.rotate_ah()
        if self.pressed["d"]: self.s2.rotate_h()
        self.canvas.update()

    def game_loop(self):
        self.check_presses()
        self.s1.update()
        self.s2.update()
        self.after(50, self.game_loop)

if __name__ == "__main__":
    jf = SpaceFighter()
    jf.mainloop()
