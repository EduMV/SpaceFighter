import tkinter as tk
from ship import Ship

class SpaceFighter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.title("Jet Fighter")
        self.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self, bg="darkblue", width=self.width, height=self.height)
        self.canvas.pack()
        self.s1 = Ship(self.canvas, "w_ship_sprites", 100, 500)
        #self.s2 = Ship(self.canvas, "b_ship_sprites", 700, 100)
        self.events_init()
        self.game_loop()

    def events_init(self):
        self.bind("<Left>", self.s1.rotate_ah)
        self.bind("<Right>", self.s1.rotate_h)

    def game_loop(self):
        self.s1.update()
        print(self.s1.get_position())
        self.after(50, self.game_loop)

    

if __name__ == "__main__":
    jf = SpaceFighter()
    jf.mainloop()
