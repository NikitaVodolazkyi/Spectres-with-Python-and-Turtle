# from turtle import Turtle, Screen
# from linear_algebra import *
# from turtle_tools import *
# import tkinter as tk
from shapes import *
import time


MAGNIFICATION = 6
STEP_LENGTH = 30
show_quad = False
is_drawing = False


# Fix the overlap when the turtle is visible, and you press reset (fixed but in a questionable way)
# Fix the overlap when is_visible = True and you press Build Supertiles many times
def draw():
    global is_drawing
    start = time.time()
    is_drawing = True
    draw_type = clicked.get()
    turtle.clear()
    if int(is_visible.get()):
        screen.tracer(14)
    else:
        screen.tracer(False)

    base[draw_type].draw(MAGNIFICATION * IDENT)
    if show_quad:
        for child in base[draw_type].children:
            draw_polygon(child['tile'].quad, T=MAGNIFICATION * child['transf'],
                         pen_colour='red')

    screen.tracer(True)
    is_drawing = False
    print(time.time() - start)


def supertile():
    global base
    base = build_supertiles(base)
    draw()


def reset():
    global base
    if not is_drawing:
        base = build_spectre_base()
        draw()


def move_left():
    canvas.xview_scroll(-1, "units")


def move_right():
    canvas.xview_scroll(1, "units")


def move_up():
    canvas.yview_scroll(-1, "units")


def move_down():
    canvas.yview_scroll(1, "units")


canvas.config(yscrollincrement=str(STEP_LENGTH))
canvas.config(xscrollincrement=str(STEP_LENGTH))


if __name__ == "__main__":

    clicked = tk.StringVar()
    clicked.set("Gamma")

    is_visible = tk.StringVar(value='0')
    checkbut_visible = tk.Checkbutton(root, variable=is_visible, text='Show turtle')
    checkbut_visible.place(x=0, y=75)

    # select_panel = tk.Frame(root, width=200, height=500, bg='red', borderwidth=10)
    # select_panel.pack(fill='both', side='left')
    # select_panel.place(x=0, y=0)

    but = tk.Button(root, text="Build Supertiles", command=supertile)
    but.place(x=0, y=0)

    reset = tk.Button(root, text="Reset", command=reset)
    reset.place(x=0, y=25)

    spectre_types = [
        'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi',
        'Pi', 'Sigma', 'Phi', 'Psi']

    drop = tk.OptionMenu(root, clicked, *spectre_types)
    drop.place(x=0, y=50)

    base = build_spectre_base()
    draw()

    screen.listen()

    screen.onkeypress(move_left, "Left")
    screen.onkeypress(move_right, "Right")
    screen.onkeypress(move_up, "Up")
    screen.onkeypress(move_down, "Down")
    screen.onkey(root.destroy, "Escape")

    screen.mainloop()
