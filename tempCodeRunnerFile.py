def circle_pop(click_event):
    x = click_event.x
    y = click_event.y
    r = 30
    canvas = click_event.widget
    items = canvas.find_overlapping(x-r, y-r, x+r, y+r)
    if items:
        for item in items:
            if canvas.type(item) == "oval":
                canvas.delete(item)
                generate_random_circle(canvas)
                break