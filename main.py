# from turtle import Turtle, Screen
# from LinearAlgebra import *
# from TurtleTools import *
from Shapes import *
import time

'''
Ideas:
For testing stuff consider first writing an interactive window and then doing the drawing.

To create seemingly infinite grid use large enough(calculated using resolution)
metatiles so they will fill the whole space. Delete the ones out of view.
(? how to deal with the edges of large supertiles tho)

Create a menu for interactions with the user

I like the idea of creating class Meta and building shapes using functions instead
and connecting them using quads

do i put colmaps in classes?     e.g.:
t1 = Tile(0, "Phi", 0, 30)
Tile.change_palette("Phi", (0, 0, 0))

How to raise an error if the type of an attribute is invalid

To do:
Create a github and put it with the guide, papers on tiles in the onenote
'''

# ! There is a problem with quads because of the reflection that I don't want to use
# Just figure out a way to fix it because I don't want to reflect it bruh

# Btw the turtle takes 1800 times more time to draw it than it takes to create the instances of supertiles
# If we want to optimise I'd consider changing the library
# Actually it's not quite true because there are also lots of matrix multiplications going on (not that much)
# Would be nice to optimise them (e.g. cache)

# Look at the start poly method in turtle
# by making many turtle instances draw each tile/supertile (now there's only 1)
# Explore how to create buttons with turtle/can we implement dragging?
# Look at the register_shape method
# I did something and now th code for 5 runs 2 times faster. Maybe other apps on my laptop affect performance

# I fixed the reflection thing using rev(short for reversed)
# but for some reason it doesn't exactly draw supertiles at the same position, I'll have to check it

start = time.time()

MAGNIFICATION = 10

width, height = screen.screensize()
screen.screensize(width * MAGNIFICATION, height * MAGNIFICATION)

n = 4
base = build_spectre_base()
for i in range(n):
    base = build_supertiles(base)

    # for key in base.keys():
    #     draw_polygon(base[key].quad, pen_colour="red")
    #     break
    # sleep(2)
    # screen.clear()
print(time.time() - start)

screen.tracer(False)

base['Xi'].draw(ident)
screen.tracer(True)

print(time.time() - start)
print(screen.turtles())


# I'm using MAGNIFICATION incorrectly and also the code below for some reason makes the turtle draw random lines

def move_left():
    canvas.xview_scroll(-1, "units")


def move_right():
    canvas.xview_scroll(1, "units")


def move_up():
    canvas.yview_scroll(-1, "units")


def move_down():
    canvas.yview_scroll(1, "units")


canvas = screen.getcanvas()
canvas.config(xscrollincrement=str(MAGNIFICATION))
canvas.config(yscrollincrement=str(MAGNIFICATION))

screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")

screen.listen()

screen.mainloop()
