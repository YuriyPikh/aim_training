import tkinter as tk
import random
import time

class Circle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(50, 550)
        self.y = random.randint(50, 350)
        self.r = random.randint(10, 30)
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
        self.points = 0
        self.start_time = int(time.time() * 1000)
        self.running = True

        self.points_label = tk.Label(self.canvas, text="Points: 0", bg="grey", font=("Segoe UI", 12))
        self.points_label.place(relx=0.01, rely=0.01)

        self.loop()

    def loop(self):
        if not self.running:
            return

        now = int(time.time() * 1000)

        # Видалити застарілі кола
        for circle in self.circles[:]:
            if circle.is_expired(now, self.CIRCLE_TTL):
                circle.remove()
                self.circles.remove(circle)

        # Створити нове коло
        self.spawn_circle()

        if now - self.start_time < self.GAME_DURATION:
            self.canvas.after(self.SPAWN_INTERVAL, self.loop)
        else:
            self.points_label.place_forget()
            self.end_game()

    def spawn_circle(self):
        circle = Circle(self.canvas)
        self.circles.append(circle)

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
