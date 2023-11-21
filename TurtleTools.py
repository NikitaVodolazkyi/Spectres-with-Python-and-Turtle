from turtle import Turtle, Screen
from LinearAlgebra import *

turtle = Turtle(visible=False)
screen = Screen()


# This function must be changed. I created it temporarily, and we should use another tool to change the scale
# At least use matrix multiplication for translating/scaling/rotating the camera (even better to use tkinter)
def enlarge(scale_factor: float, shape: tuple) -> tuple:
    return tuple(pt(scale_factor * p["x"], scale_factor * p["y"]) for p in shape)


def get_init_settings() -> tuple:
    """
    Returns initial pen state (isdown), position, heading of the turtle
    """
    return turtle.isdown(), turtle.position(), turtle.heading()


def teleport(x: float, y: float) -> None:
    in_down = turtle.isdown()
    turtle.penup()
    turtle.goto(x, y)

    if in_down:
        turtle.pendown()


# Do we need to set the position back? I doubt that we will use forward, left, etc. ever
# For now I commented the code that sets everything back
# With setting things back it takes 1/8 more time (that's a lot)
# Also there is some variation in the time required for the code to draw nth gen supertile

def draw_polygon(points: tuple | list, T=None, fill=None, pen_colour=None) -> None:
    # in_down, in_pos, in_heading = get_init_settings()
    # in_fill = turtle.fillcolor

    if pen_colour is not None:
        turtle.pencolor(pen_colour)
    else:
        turtle.pencolor("black")

    if fill is not None:
        turtle.fillcolor(fill)
        turtle.begin_fill()

    if T is not None:
        polygon = [transPt(T, point) for point in points]
    else:
        polygon = points
    start = polygon[0]

    teleport(start["x"], start["y"])
    turtle.pendown()
    for p in polygon:
        turtle.goto(p["x"], p["y"])
    turtle.goto(start["x"], start["y"])

    if fill is not None:
        turtle.end_fill()

    # turtle.fillcolor = in_fill
    # teleport(*in_pos)
    # turtle.setheading(in_heading)
    # if not in_down:
    #     turtle.penup()
