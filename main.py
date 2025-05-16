import tkinter as tk
import random
import time

class Circle:
    def __init__(self, canvas, x, y, r):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.id = self.canvas.create_oval(
            self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
            fill="red", outline="black"
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
        global width, height
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg='grey', highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<ButtonRelease-1>", self.on_click)

        self.circles = []
        self.lines = []
        self.points = 0
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
        self.points_label.place(relx=0.01, rely=0.01)

        self.timer_lable = tk.Label(self.canvas, text="Time: 60", bg="grey", font=("Segoe UI", 12))
        self.timer_lable.place(relx=0.88, rely=0.01)
        self.loop()


    def define_type_of_spawn(self):
            self.type_of_spawn
            self.type_of_spawn = random.randint(0, 1)

    def loop(self):
        if not self.running:
            return

        now = int(time.time() * 1000)
        time_spent= int((now - self.start_time)) 
        # Видалити застарілі кола
        for circle in self.circles[:]:
            if circle.is_expired(now, self.CIRCLE_TTL):
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
        
        if time_spent < self.GAME_DURATION:
            self.timer_lable.config(text=f"Time: {60 - int(time_spent/1000)}")
            self.canvas.after(self.SPAWN_INTERVAL, self.loop)
        else:
            self.timer_lable.place_forget()
            self.points_label.place_forget()
            self.end_game()

    def draw_circle_line(self):
        self.line_x1 = random.randint(50, 550)
        self.line_y1 = random.randint(50, 350)
        self.line_x2 = random.randint(50, 550)
        self.line_y2 = random.randint(50, 350)
        self.line_id = self.canvas.create_line(self.line_x1, self.line_y1, self.line_x2, self.line_y2, fill="blue", width=2)
        self.lines.append(self.line_id)
    
    def destroy_lines(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        
    def random_spawn_circle(self):
        self.number_of_spawned_circles
        self.random_iteration_spawn_number

        self.number_of_spawned_circles += 1 
        x = random.randint(50, 550)
        y = random.randint(50, 350)
        r = random.randint(10, 30)
        circle = Circle(self.canvas, x, y, r)
        self.circles.append(circle)
        

    def line_spawn_circle(self , r): 
        t = self.number_of_spawned_circles / (self.random_iteration_spawn_number - 1) if self.random_iteration_spawn_number > 1 else 0.5
        x = int(self.line_x1 + (self.line_x2 - self.line_x1) * t)
        y = int(self.line_y1 + (self.line_y2 - self.line_y1) * t)
        circle = Circle(self.canvas, x, y, r)
        self.circles.append(circle)
        self.number_of_spawned_circles += 1
    
    def on_click(self, event):
        for circle in self.circles:
            if circle.is_clicked(event.x, event.y):
                circle.remove()
                self.circles.remove(circle)
                self.add_points()
                break

    def add_points(self):
        self.points += 5
        self.points_label.config(text=f"Points: {self.points}")

    def end_game(self):
        self.running = False
        self.canvas.delete("all")
        tk.Label(self.canvas, text="Time's out", bg="grey", font=("Segoe UI", 12)).place(relx=0.5, rely=0.5, anchor='center')
        tk.Label(self.canvas, text=f"Your Points: {self.points}", bg="grey", font=("Segoe UI", 12)).place(relx=0.5, rely=0.6, anchor='center')
        self.canvas.after(3000, self.reset_game)

    def reset_game(self):
        self.canvas.destroy()
        GameMenu(self.root)


class GameMenu:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=220, height=220, bg='black', highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.build_menu()

    def build_menu(self):
        label = tk.Label(self.canvas, text="Game Menu", bg="gray", font=("Segoe UI", 12))
        label.grid(row=0, column=0, padx=10, pady=10)

        start_btn = tk.Button(self.canvas, text="Start Game", bg="gray", command=self.start_game)
        start_btn.grid(row=1, column=0, padx=10, pady=5)

        exit_btn = tk.Button(self.canvas, text="Exit", bg="gray", command=root.quit)
        exit_btn.grid(row=2, column=0, padx=10, pady=5)

    def start_game(self):
        self.canvas.destroy()
        Game(self.root)



root = tk.Tk()
width = 600
height = 400
root.geometry(f"{width}x{height}")
root.title("Reaction trainer")
root.resizable(False, False)
root.configure(bg="gray")
GameMenu(root)
root.mainloop()
