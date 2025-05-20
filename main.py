import tkinter as tk
import random
import time
import colorsys


class Circle:
    circle_color = "#ff0000"
    def __init__(self, canvas, x, y, r):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        
        self.id = self.canvas.create_oval(
            self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
            fill=f"{Circle.circle_color}", outline="black"
        )
        self.spawn_time = int(time.time() * 1000)

    def is_expired(self, current_time, ttl=1000):
        return current_time - self.spawn_time >= ttl

    def is_clicked(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2 <= self.r ** 2

    def remove(self):
        self.canvas.delete(self.id)

class Game:
    CIRCLE_TTL = 1000
    SPAWN_INTERVAL = 350
    GAME_DURATION = 60000
    def __init__(self, root):
        self.root = root
        self.window_width = root.winfo_width()
        self.window_height = root.winfo_height()
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg='grey', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<ButtonRelease-1>", self.on_click)
        
        

        #часові змінні
        self.now = 0
        self.time_spent = 0

        self.circles = []
        self.lines = []
        self.hitted_circles = 0
        self.whole_number_of_circles = 0
        self.start_time = int(time.time() * 1000)
        self.running = True

        # координати лінії І радіус кола на ній
        self.line_x1 = 0
        self.line_y1 = 0
        self.line_x2 = 0
        self.line_y2 = 0
        self.line_id = 0
        self.radious_of_line_circle = 20
        #кількість кіл які потрібно заспавнити
        self.random_iteration_spawn_number = random.randint(5, 15)
        # Кількість вже заспавнених кіл 
        self.number_of_spawned_circles = 0
        # Випадковий тип спавну 0 - рандомнийб 1- лінійний
        self.type_of_spawn = 0

        self.points_label = tk.Label(self.canvas, text="Points: 0", bg="grey", font=("Segoe UI", 12))
        self.points_label.place(x=10, y=10)

        self.timer_lable = tk.Label(self.canvas, text="Time: 60", bg="grey", font=("Segoe UI", 12))
        self.timer_lable.place(relx=1.0, x=-10, y=10, anchor='ne')

        #press esc to pause
        self.root.bind("<Escape>", lambda event: self.canvas.after(0, self.build_pouse_menu()))
        self.loop()


    def define_type_of_spawn(self):
            self.type_of_spawn
            self.type_of_spawn = random.randint(0, 1)

    def loop(self):
        if not self.running:
            return



        self.now = int(time.time() * 1000)
        self.time_spent= int((self.now - self.start_time)) 
        # Видалити застарілі кола
        for circle in self.circles[:]:
            if circle.is_expired(self.now, self.CIRCLE_TTL):
                circle.remove()
                self.circles.remove(circle)

        

        if self.type_of_spawn == 0:
            self.destroy_lines()
            self.random_spawn_circle()
            if self.number_of_spawned_circles == self.random_iteration_spawn_number :
                self.number_of_spawned_circles = 0
                self.define_type_of_spawn()
                self.random_iteration_spawn_number = random.randint(5, 15)
        else:
            
            if self.number_of_spawned_circles == 0 : self.draw_circle_line() 
            self.line_spawn_circle(self.radious_of_line_circle)  
            if self.number_of_spawned_circles == self.random_iteration_spawn_number :
                self.number_of_spawned_circles = 0
                self.type_of_spawn = random.randint(0, 1)
                self.radious_of_line_circle = random.randint(10, 30)
                self.random_iteration_spawn_number = random.randint(5, 15)
        
        
        if self.time_spent < self.GAME_DURATION:
            self.timer_lable.config(text=f"Time: {60 - int(self.time_spent/1000)}")
            self.canvas.after(self.SPAWN_INTERVAL, self.loop)
        else:
            self.timer_lable.place_forget()
            self.points_label.place_forget()
            self.end_game()

    def draw_circle_line(self):
        self.line_x1 = random.randint(50, self.window_width - 50)
        self.line_y1 = random.randint(50, self.window_height - 50)
        self.line_x2 = random.randint(50, self.window_width - 50)
        self.line_y2 = random.randint(50, self.window_height - 50)
        self.line_id = self.canvas.create_line(self.line_x1, self.line_y1, self.line_x2, self.line_y2, fill="white", width=2)
        self.lines.append(self.line_id)
        # Calculate the distance between the two points
        line_length = ((self.line_x2 - self.line_x1) ** 2 + (self.line_y2 - self.line_y1) ** 2) ** 0.5
        # Number of circles so that they just touch each other along the line
        if self.radious_of_line_circle > 0:
            self.random_iteration_spawn_number = max(2, int(line_length // (2 * self.radious_of_line_circle)) + 1)
        else:
            self.random_iteration_spawn_number = 2
    
    def destroy_lines(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        
    def random_spawn_circle(self):
        self.number_of_spawned_circles
        self.random_iteration_spawn_number

        self.number_of_spawned_circles += 1 
        x = random.randint(50, self.window_width - 50)
        y = random.randint(50, self.window_height - 50)
        r = random.randint(10, 30)
        circle = Circle(self.canvas, x, y, r)
        self.circles.append(circle)
        self.whole_number_of_circles += 1
        

    def line_spawn_circle(self , r): 
        t = self.number_of_spawned_circles / (self.random_iteration_spawn_number - 1) if self.random_iteration_spawn_number > 1 else 0.5
        x = int(self.line_x1 + (self.line_x2 - self.line_x1) * t)
        y = int(self.line_y1 + (self.line_y2 - self.line_y1) * t)
        circle = Circle(self.canvas, x, y, r)
        self.circles.append(circle)
        self.number_of_spawned_circles += 1
        self.whole_number_of_circles += 1
    
        '''    def spawn_drag_box_and_circle(self):
            # Remove any previous drag box or circles
            self.destroy_lines()
            for circle in self.circles[:]:
                circle.remove()
                self.circles.remove(circle)

            # Define box dimensions
            box_width = random.randint(120, 200)
            box_height = random.randint(40, 80)
            margin = 40
            x1 = random.randint(margin, width - box_width - margin)
            y1 = random.randint(margin, height - box_height - margin)
            x2 = x1 + box_width
            y2 = y1 + box_height

            # Draw the box (rectangle)
            self.drag_box_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=3)
            self.lines.append(self.drag_box_id)

            # Spawn a circle at the left edge of the box
            r = 20
            circle_x = x1 + r
            circle_y = (y1 + y2) // 2
            self.drag_circle_obj = Circle(self.canvas, circle_x, circle_y, r)
            self.circles.append(self.drag_circle_obj)

            # Store drag box info for use in drag event
            self.drag_box = (x1, y1, x2, y2)
            self.dragging = False

            # Bind mouse events for dragging
            self.canvas.bind("<ButtonPress-1>", self.start_drag)
            self.canvas.bind("<B1-Motion>", self.do_drag)
            self.canvas.bind("<ButtonRelease-1>", self.stop_drag)

        def start_drag(self, event):
            # Only start drag if click is inside the circle
            if hasattr(self, 'drag_circle_obj') and self.drag_circle_obj.is_clicked(event.x, event.y):
                self.dragging = True

        def do_drag(self, event):
            if getattr(self, 'dragging', False) and hasattr(self, 'drag_circle_obj'):
                x1, y1, x2, y2 = self.drag_box
                r = self.drag_circle_obj.r
                # Clamp x within box
                new_x = min(max(event.x, x1 + r), x2 - r)
                # Keep y centered in the box
                new_y = (y1 + y2) // 2
                self.canvas.coords(
                    self.drag_circle_obj.id,
                    new_x - r, new_y - r,
                    new_x + r, new_y + r
                )
                self.drag_circle_obj.x = new_x
                self.drag_circle_obj.y = new_y

        def stop_drag(self, event):
            if getattr(self, 'dragging', False) and hasattr(self, 'drag_circle_obj'):
                x1, y1, x2, y2 = self.drag_box
                r = self.drag_circle_obj.r
                # If circle is at the right edge of the box, count as hit
                if self.drag_circle_obj.x >= x2 - r - 2:
                    self.drag_circle_obj.remove()
                    self.circles.remove(self.drag_circle_obj)
                    self.add_points()
                    # Remove box
                    self.canvas.delete(self.drag_box_id)
                    self.lines.clear()   
                self.dragging = False'''


    def on_click(self, event):
        for circle in self.circles:
            if circle.is_clicked(event.x, event.y):
                circle.remove()
                self.circles.remove(circle)
                self.add_points()
                break


    def add_points(self):
        self.hitted_circles += 1
        self.points_label.config(text=f"Points: {self.hitted_circles*5}")

    def end_game(self):
        self.running = False
        self.canvas.delete("all")
        tk.Label(self.canvas, text="Time's out", bg="grey", font=("Segoe UI", 12)).place(relx=0.5, rely=0.3, anchor='center')
        tk.Label(self.canvas, text=f"Your Points: {self.hitted_circles*5}", bg="grey", font=("Segoe UI", 12)).place(relx=0.5, rely=0.4, anchor='center')
        tk.Label(self.canvas, text=f"Your Accuracy: {int((self.hitted_circles * 100)/self.whole_number_of_circles)} %", bg="grey", font=("Segoe UI", 12)).place(relx=0.5, rely=0.5, anchor='center')
        self.canvas.after(5000, self.reset_game)

    def reset_game(self):
        self.canvas.destroy()
        GameMenu(self.root)

    def build_pouse_menu(self):
        
        self.stop_game_loop()
        #unbind escape key 
        self.canvas_for_manue = tk.Canvas(root, width=220, height=220, bg='black', highlightthickness=0)
        self.canvas_for_manue.place(relx=0.5, rely=0.5, anchor='center')
        pouse_label = tk.Label(self.canvas_for_manue, text="Paused", bg="gray", font=("Segoe UI", 12))
        pouse_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        pouse_resume_btn = tk.Button(self.canvas_for_manue, text="Resume", bg="gray", command=self.resume_game)
        pouse_resume_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        pouse_exit_btn = tk.Button(self.canvas_for_manue, text="Exit to Menu", bg="gray", command=self.exit_to_menu)
        pouse_exit_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    def resume_game(self):
        self.canvas_for_manue.destroy()
        self.running = True
        self.loop()

    def exit_to_menu(self):
        self.canvas_for_manue.destroy()
        self.canvas.destroy()
        GameMenu(self.root)
        
    def stop_game_loop(self):
        self.running = False

class GameMenu:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=220, height=220, bg='black', highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.build_menu()

    def build_menu(self):
        label = tk.Label(self.canvas, text="Game Menu", bg="gray", font=("Segoe UI", 12))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        start_btn = tk.Button(self.canvas, text="Start Game", bg="gray", command=self.start_game)
        start_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        start_btn = tk.Button(self.canvas, text="Game Settings", bg="gray", command=self.open_settings)
        start_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        exit_btn = tk.Button(self.canvas, text="Exit", bg="gray", command=root.quit)
        exit_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    def start_game(self):
        self.canvas.destroy()
        Game(self.root)

    def open_settings(self):
        self.canvas.destroy()
        settings_canvas = tk.Canvas(self.root, width=220, height=220, bg='black', highlightthickness=0)
        settings_canvas.place(relx=0.5, rely=0.5, anchor='center')
        label = tk.Label(settings_canvas, text="Settings", bg="gray", font=("Segoe UI", 12))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


        difficulty_label = tk.Label(settings_canvas, text="Difficulty Level:", bg="gray", font=("Segoe UI", 10))
        difficulty_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        difficulty_var = tk.StringVar(value="Normal")
        difficulty_spinbox = tk.Spinbox(
            settings_canvas,
            values=("Easy", "Normal", "Hard"),
            textvariable=difficulty_var,
            state="readonly",
            width=5,
            font=("Segoe UI", 10)
        )
        difficulty_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        color_label = tk.Label(settings_canvas, text="Target Color:", bg="gray", font=("Segoe UI", 10))
        color_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

        # Default color is red (hue=0)
        hue_var = tk.DoubleVar(value=0.0)

        def hue_to_hex(h):
            # Convert hue [0,1] to RGB, then to hex
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

        color_preview = tk.Label(settings_canvas, bg=hue_to_hex(hue_var.get()), width=10, height=2)
        color_preview.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        def update_preview(val):
            color_preview.config(bg=hue_to_hex(float(val)))

        hue_slider = tk.Scale(settings_canvas, from_=0, to=1, resolution=0.01, orient="horizontal", bg="gray",
                      variable=hue_var, command=update_preview, length=150)
        hue_slider.grid(row=3, column=1, padx=5, pady=5)

        def apply_changes():
            Circle.circle_color = hue_to_hex(hue_var.get())
            color_preview.config(bg=Circle.circle_color)
            
            if difficulty_var.get() == "Easy":
                    Game.SPAWN_INTERVAL = 500
                    Game.CIRCLE_TTL = 1500
            elif difficulty_var.get() == "Normal":
                    Game.SPAWN_INTERVAL = 350
                    Game.CIRCLE_TTL = 1000
            elif difficulty_var.get() == "Hard":
                    Game.SPAWN_INTERVAL = 200
                    Game.CIRCLE_TTL = 700
            
            if screen_mode_var.get() == "Windowed":
                self.root.geometry = f"{width}x{height}"
                self.root.attributes('-fullscreen', False)
            elif screen_mode_var.get() == "Fullscreen":
                width, height = self.root.winfo_screenwidth() , self.root.winfo_screenheight()
                self.root.attributes('-fullscreen', True)

        color_label = tk.Label(settings_canvas, text="Sreen mode:", bg="gray", font=("Segoe UI", 10))
        color_label.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        screen_mode_var = tk.StringVar(value="Windowed")
        screen_mode_spinbox = tk.Spinbox(
            settings_canvas,
            values=("Windowed", "Fullscreen"),
            textvariable=screen_mode_var,
            state="readonly",
            width=10,
            font=("Segoe UI", 10)
        )
        screen_mode_spinbox.grid(row=4, column=1, padx=5, pady=5, sticky="ew")


        apply_btn = tk.Button(settings_canvas, text="Apply Changes", bg="gray", command=apply_changes)
        apply_btn.grid(row=5, column=0, padx=5, pady=5, sticky="ew")


        back_btn = tk.Button(settings_canvas, text="Back", bg="gray", command=lambda: back_to_menu(self, settings_canvas))
        back_btn.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        def back_to_menu(self, settings_canvas):
            settings_canvas.destroy()
            GameMenu(self.root)
    

root = tk.Tk()
global width, height
width = 600
height = 400
root.geometry(f"{width}x{height}")
root.title("Reaction trainer")
root.resizable(False, False)
root.configure(bg="gray")
GameMenu(root)
root.mainloop()
