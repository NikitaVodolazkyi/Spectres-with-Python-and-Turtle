from turtle import RawTurtle, TurtleScreen
from linear_algebra import *
import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=19800, height=10800)

canvas.pack()
root.attributes("-fullscreen", True)

screen = TurtleScreen(canvas)
screen.colormode(255)
screen_width = screen.window_width()
screen_height = screen.window_height()

canvas.xview_scroll(-5, "units")
canvas.yview_scroll(-5, "units")

turtle = RawTurtle(screen, visible=False)


# def get_init_settings() -> tuple:
#     """
#     Returns initial pen state (isdown), position, heading of the turtle
#     """
#     return turtle.isdown(), turtle.position(), turtle.heading()


def teleport(x: float, y: float) -> None:
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()


# There is some variation in the time required for the code to draw nth gen supertile
def draw_polygon(points: tuple | list, T: Matrix = None, fill=None, pen_colour=None) -> None:
    if pen_colour is not None:
        turtle.pencolor(pen_colour)
    else:
        turtle.pencolor("black")

    if fill is not None:
        turtle.fillcolor(fill)
        turtle.begin_fill()

    if T is not None:
        polygon = [T * point for point in points]
    else:
        polygon = points

    start = polygon[0]

    teleport(start.x, start.y)
    for p in polygon:
        turtle.goto(p.x, p.y)
    turtle.goto(start.x, start.y)

    if fill is not None:
        turtle.end_fill()
