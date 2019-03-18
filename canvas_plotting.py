# plot a function like y = sin(x) with Tkinter canvas and line

from tkinter import *
import math
import time

root = Tk()
root.title("Simple plot using canvas and line")

width = 400
height = 300
center = height//2
x_increment = 1
# width stretch
x_factor = 0.04
# height stretch
y_amplitude = 80

c = Canvas(width=width, height=height, bg='white')
c.pack()

str1 = "sin(x)=blue"
c.create_text(10, 20, anchor=SW, text=str1)

center_line = c.create_line(0, center, width, center, fill='green')

# create the coordinate list for the sin() curve, have to be integers
xy1 = []
for x in range(400):
    # x coordinates
    xy1.append(x * x_increment)
    # y coordinates
    xy1.append(int(math.sin(x * x_factor) * y_amplitude) + center)

sin_line = c.create_line(xy1, fill='blue')
root.mainloop()
