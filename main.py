import tkinter as tk
import random
import time

root = tk.Tk()
width_root = 600
height_root = 400
root.geometry(f"{width_root}x{height_root}")
root.title("Reaction trainer")
root.resizable(False, False)
root.configure(bg="gray")
root.attributes("-toolwindow",0)

CIRCLE_TTL = 1000  
SPAWN_INTERVAL = 350  
GAME_DURATION = 60000

circles = [] 
game_running = False
game_start_time = 0

point_counter = 0



def exit_click():
    root.quit()

def create_game_manue():
    global game_menu_canva
    game_menu_canva = tk.Canvas(root, width=220, height=220, bg='black', highlightthickness=0)
    game_menu_canva.place(relx=0.5, rely=0.5, anchor='center')

    label = tk.Label(game_menu_canva, text="Game Menu", bg="gray", font=("Segoe UI", 12))
    label.grid(row=0, column=0, padx=10, pady=10, sticky="we")

    start_button = tk.Button(game_menu_canva, text="Start Game", bg="gray", command=define_start_game)
    start_button.grid(row=1, column=0, padx=10, pady=5, sticky="we")

    exit_button = tk.Button(game_menu_canva, text="Exit", command=exit_click, bg="gray")
    exit_button.grid(row=2, column=0, padx=10, pady=5, sticky="we")
    game_menu_canva.place(relx=0.5, rely=0.5, anchor='center')

def remove_expired_circles(canvas):
    now = int(time.time() * 1000)
    expired = []
    for circle_id, spawn_time in circles:
        if now - spawn_time >= CIRCLE_TTL:
            canvas.delete(circle_id)
            expired.append((circle_id, spawn_time))
    for item in expired:
        circles.remove(item)

def spawn_circle(canvas):
    x = random.randint(50, 550)
    y = random.randint(50, 350)
    r = random.randint(10, 30)
    circle_id = canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", outline="black", width=1)
    spawn_time = int(time.time() * 1000)
    circles.append((circle_id, spawn_time))

        


def circle_pop(click_event):
    x = click_event.x
    y = click_event.y
    r = 5
    canvas = click_event.widget
    items = canvas.find_overlapping(x-r, y-r, x+r, y+r)
    for item in items:
        if canvas.type(item) == "oval":
            canvas.delete(item)
            update_point_counter()
            for circle in circles:
                if circle[0] == item:
                    circles.remove(circle)
                    break

def define_start_game():
    global circles, game_running, game_start_time, game_canvas
    circles = []
    game_running = True
    game_start_time = int(time.time() * 1000)
    game_menu_canva.place_forget()
    game_canvas = tk.Canvas(root, width=width_root, height=height_root, bg='grey', highlightthickness=0)
    game_canvas.place(relx=0.5, rely=0.5, anchor='center')
    game_canvas.bind("<ButtonRelease-1>", circle_pop)
    global point_counter_label
    point_counter_label = tk.Label(game_canvas, text=f"Points: {point_counter}", bg="grey", font=("Segoe UI", 12))
    point_counter_label.place(relx=0.01, rely=0.01)
    game_loop(game_canvas)

def update_point_counter():
    global point_counter, point_counter_label
    point_counter += 5
    point_counter_label.config(text=f"Points: {point_counter}")

def flush_point_counter():
    global point_counter
    point_counter = 0
    point_counter_label.place_forget()

def game_loop(canvas):
    global game_running
    if not game_running:
        return
    remove_expired_circles(canvas)
    spawn_circle(canvas)
    now = int(time.time() * 1000)
    if now - game_start_time < GAME_DURATION:
        canvas.after(SPAWN_INTERVAL, lambda: game_loop(canvas))
    else:
        point_counter_label.place_forget()
        end_game(canvas)



def end_game(canvas):
    global game_running
    game_running = False
    canvas.delete("all")
    point_counter_label = tk.Label(game_canvas, text="Time's out", bg="grey", font=("Segoe UI", 12))
    point_counter_label.place(relx=0.5, rely=0.5, anchor='center')
    point_counter_label = tk.Label(game_canvas, text=f"Your Points: {point_counter}", bg="grey", font=("Segoe UI", 12))
    point_counter_label.place(relx=0.5, rely=0.55, anchor='center')
    canvas.after(2000, lambda: [canvas.destroy(), create_game_manue()])
    flush_point_counter()

create_game_manue()
root.mainloop()

