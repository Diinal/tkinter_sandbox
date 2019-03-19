# plot a function like y = sin(x) with Tkinter canvas and line

from tkinter import *
import math
import random, time, sys

root = Tk()
root.title("Simple plot using canvas and line")

def win_dstr():
    root.destroy()


width = 400
height = 300
center = height//2
x_increment = 1
# width stretch
x_factor = 0.1
# height stretch
y_amplitude = 80


def chg_amp():
    global y_amplitude
    y_amplitude *= 2

c = Canvas(width=width, height=height, bg='white')
c.pack()

str1 = "sin(x)=blue"
c.create_text(10, 20, anchor=SW, text=str1)
button = Button(text = 'amp x2', command = chg_amp)
button.pack()

center_line = c.create_line(0, center, width, center, fill='green', arrow = LAST)

# create the coordinate list for the sin() curve, have to be integers
xy1 = []
for x in range(400):
    # x coordinates
    xy1.append(x * x_increment)
    # y coordinates
    xy1.append(int(math.sin(x * x_factor) * y_amplitude) + center)

#sin_line = c.create_line(xy1, fill='blue')

x = [i for i in range(400)]
'''
y = [int(math.sin((i+10) * x_factor) * y_amplitude) + center for i in x]
xy = list(zip(x, y))
sin_line = c.create_line(xy, fill='blue')
sin_line2 = c.create_line(xy1, fill = 'red')'''
frame = 0
while True:
    try:
        y = [int(math.sin((i+frame) * x_factor) * y_amplitude * .5) + center for i in x]
        xy = list(zip(x, y))
        sin_line = c.create_line(xy, fill = 'red', width = 1)
        if frame < 125:
            frame += 1
        else:
            frame = 0
        root.update()
        time.sleep(.01)
        c.delete(sin_line)
    except Exception:
        sys.exit(0)

root.protocol("WM_DELETE_WINDOW", win_dstr)

root.mainloop()
