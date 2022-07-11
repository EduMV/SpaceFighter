import tkinter as tk
from PIL import ImageTk, Image
from ship import Ship

class SpaceFighter(tk.Tk):

    i_lives_steps = [1, 3, 5, 10, 15, 20, 25, 30]
    velocity_steps = [1, 3, 5, 7, 10]
    cooldown_steps = [0.2, 0.4, 0.8, 1.0, 1.3, 1.5, 1.8]
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.title("Space Fighter")
        self.geometry(f"{self.width}x{self.height}")
        self.settings={
            "i_lives": 5,
            "velocity": 3,
            "cooldown": 0.8
        }
        self.b_bg = "#003b59"
        self.configure(bg=self.b_bg)
        self.frame = tk.Frame(self,bg=self.b_bg, width=self.width, height=self.height)
        self.mainmenu_screen()
        

    def mainmenu_screen(self):
        
        self.frame.destroy()
        b_font = ("Consolas", 25, "bold")
        self.frame = tk.Frame(self,bg=self.b_bg, width=self.width, height=self.height)
        self.frame.pack()
        canvas = tk.Canvas(self.frame,highlightbackground=self.b_bg ,bg=self.b_bg, width=self.width, height=self.height/2)
        canvas.pack(pady=0)
        self.title_img = ImageTk.PhotoImage(Image.open("other_sprites/title.png"))
        canvas.create_image(self.width/2, self.height/4, image=self.title_img)
        f1 = tk.Frame(self.frame, bg=self.b_bg, width=self.width, height=self.height/2)
        f1.pack(fill=tk.BOTH, pady=0)

        colors = [("#ff8531","#fbf236"),("#2d4bff","#00ffd7"),("#c82727","#921c1c")]
        b_options = ["JUGAR", "CONFIGURAR", "SALIR"]
        b_dict = {}
        for i, text in enumerate(b_options):
            b_dict[text] = tk.Button(f1,borderwidth=5, bg=colors[i][0],activebackground=colors[i][1] ,text=text, width=15,font=b_font)
            b_dict[text].pack(pady=12)

        b_dict["JUGAR"].configure(command=self.game_init)
        b_dict["CONFIGURAR"].configure(command=self.config_screen)
        b_dict["SALIR"].configure(command=self.destroy)

    def config_screen(self):
        self.op_vars = [tk.StringVar() for i in range(3)]
        self.op_vars[0].set(str(self.settings["i_lives"]))
        self.op_vars[1].set(str(self.settings["velocity"]))
        self.op_vars[2].set(str(self.settings["cooldown"]))
        self.frame.destroy()
        self.frame = tk.Frame(self,bg=self.b_bg, width=self.width, height=self.height)
        self.frame.pack(ipady=0)
        t_font = ("Consolas", 40, "bold")
        l1 = tk.Label(self.frame, text="Configurar juego", font=t_font, bg=self.b_bg)
        l1.grid(column=0, row=0, columnspan=6, ipady=80)
        config_options = ["Vidas", "Velocidad", "Cooldown"]
        self.config_dict_options = ["i_lives", "velocity", "cooldown"]
        op_font = ("Consolas", 15, "bold")
        for i, op in enumerate(config_options):
            l_op = tk.Label(self.frame, text=op, font=op_font, bg=self.b_bg, fg="#ff8531", width=10)
            l_op.grid(column=2*i, row=1, columnspan=2)
            l_var = tk.Label(self.frame, textvariable=self.op_vars[i], font=op_font, bg=self.b_bg, fg="#ff8531", width=10)
            l_var.grid(column=2*i, row=2, columnspan=2)

        b_colors = ("#c82727","#921c1c")
        b_font = ("Consolas", 10, "bold")
        b_dict = {}
        for i, op in enumerate(config_options):
            buttons = [tk.Button(self.frame,borderwidth=2, bg=b_colors[0],activebackground=b_colors[1]
                        ,text=sym, width=3,font=b_font) for sym in ["-", "+"]]
            b_dict[op] = tuple(buttons)
            
            b_dict[op][0].grid(column=2*i, row=3)
            b_dict[op][1].grid(column=2*i + 1, row=3)

        b_dict["Vidas"][0].configure(command=lambda: self.change_settings(self.config_dict_options[0], -1))
        b_dict["Vidas"][1].configure(command=lambda: self.change_settings(self.config_dict_options[0], +1))
        b_dict["Velocidad"][0].configure(command=lambda: self.change_settings(self.config_dict_options[1], -1))
        b_dict["Velocidad"][1].configure(command=lambda: self.change_settings(self.config_dict_options[1], +1))
        b_dict["Cooldown"][0].configure(command=lambda: self.change_settings(self.config_dict_options[2], -1))
        b_dict["Cooldown"][1].configure(command=lambda: self.change_settings(self.config_dict_options[2], +1))


        b = tk.Button(self.frame,borderwidth=5, bg=b_colors[0],activebackground=b_colors[1],
                    text="Volver", width=10,font=op_font, command=self.mainmenu_screen)
        b.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=100)
    
    def change_settings(self, setting, change):
        if setting == "i_lives":
            j = 0
            steps = self.i_lives_steps
        elif setting == "velocity":
            j = 1
            steps = self.velocity_steps
        elif setting == "cooldown":
            j = 2
            steps = self.cooldown_steps

        val = float(self.op_vars[j].get())
        i = steps.index(val)
        i += change
        if i < len(steps) and i>-1:
            new_val = steps[i]
            self.op_vars[j].set(new_val)
            self.settings[setting] = new_val
    
    def game_init(self):
        self.stop_game = False
        self.frame.destroy()
        self.frame = tk.Canvas(self, bg=self.b_bg, width=self.width, height=self.height)
        self.canvas = self.frame
        self.canvas.pack()
        self.s1 = Ship(self, self.canvas, self.settings,"w_ship_sprites", 100, 500, 270)
        self.s2 = Ship(self, self.canvas, self.settings,"b_ship_sprites", 700, 100, 90)

        self.s1_icontkimg = ImageTk.PhotoImage(Image.open("other_sprites/w_shipicon.png"))
        self.s1_icon = self.canvas.create_image(60, 20, image=self.s1_icontkimg)
        self.s2_icontkimg  = ImageTk.PhotoImage(Image.open("other_sprites/b_shipicon.png"))
        self.s2_icon = self.canvas.create_image(120, 20, image=self.s2_icontkimg)

        font = ("Consolas", 25, "bold")
        self.s1_lives_text = self.canvas.create_text(40, 20, text=str(self.s1.lives), font=font)
        self.s2_lives_text = self.canvas.create_text(100, 20, text=str(self.s2.lives), font=font)
        self.pressed = {}
        self.bindings_init()
        self.game_loop()

    def stop(self):
        self.stop_game = True
        self.pressed = {}
        self.unbind("<space>", self.spacebind)
        self.mainmenu_screen()
    
    def pause(self, event):
        if not self.stop_game:
            self.stop_game = True
            self.pause_tkimg = ImageTk.PhotoImage(Image.open("other_sprites/pause.png"))
            self.pause = self.canvas.create_image(self.width/2, self.height/2, image=self.pause_tkimg)
        else:
            self.canvas.delete(self.pause)
            self.stop_game = False
            self.game_loop()
        

    def bindings_init(self):
        # movimiento
        for key in ["a", "d", "j", "l", "c", "m", "Escape"]:
            self.bind(f"<KeyPress-{key}>", self.key_pressed)
            self.bind(f"<KeyRelease-{key}>", self.key_released)
            self.pressed[key] = False

        self.spacebind = self.bind("<space>", self.pause)

    def key_pressed(self, event):
        self.pressed[event.keysym] = True

    def key_released(self, event):
        self.pressed[event.keysym] = False
    
    def check_presses(self):
        if self.pressed["Escape"]:
            self.stop()
        else:
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
    
    def display_lives(self):
        font = ("Consolas", 25, "bold")
        self.canvas.delete(self.s1_lives_text)
        self.canvas.delete(self.s2_lives_text)
        self.s1_lives_text = self.canvas.create_text(40, 20, text=str(self.s1.lives), font=font)
        self.s1_lives_text = self.canvas.create_text(100, 20, text=str(self.s2.lives), font=font)

    def game_loop(self):
        if self.stop_game: return    
        self.s1.update()
        self.s2.update()
        self.display_lives()
        self.check_ship_colisions()
        self.check_presses()
        self.after(50, self.game_loop)

if __name__ == "__main__":
    sf = SpaceFighter()
    sf.mainloop()
