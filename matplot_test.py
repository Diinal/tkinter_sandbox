#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports

fig = plt.Figure()

x = np.arange(0, 10, 0.01)        # x-array

def animate1(i):
    line.set_ydata(np.sin(x+i/50.0))  # update the data 10.0
    #line2.set_ydata(np.sin((x+i/50.0)*freq)*amp)
    return line,

def animate2(i):
    line2.set_ydata(np.sin((x+i/50.0)*freq)*amp)
    return line2,

def animate3(i):
    y_signal = np.sin(x+i/50.0) + 1 #1 is previus y_max, it's need for up signal line
    y_max = max(y_signal)
    y_carry = np.sin((x+i/50.0)*freq)*amp*(y_signal/y_max)
    line3.set_ydata(y_carry)
    line4.set_ydata(np.sin(x+i/50.0)+1)
    return line3, line4,


def normalize(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(-3, 3)
    #ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    #ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

root = Tk.Tk()

Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,row=1)

ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
normalize(ax)
normalize(ax2)
normalize(ax3)
freq = 10
amp = 2
line, = ax.plot(x, np.sin(x))
max_signal_amp = max(np.sin(x))
line2, = ax2.plot(x, np.sin(x*freq)*amp)

y_max = max(np.sin(x)+1)
y_signal = np.sin(x) + 1
y_carry = np.sin(x*freq)*amp*(y_signal/y_max)
line3, = ax3.plot(x, y_carry)
line4, = ax3.plot(x, y_signal)

ani1 = animation.FuncAnimation(fig, animate1, np.arange(1, 310), interval=20, blit=True)
ani2 = animation.FuncAnimation(fig, animate2, np.arange(1, 32), interval=20, blit=True) #if speed = 10.0 => range = 125, interval =20
ani3 = animation.FuncAnimation(fig, animate3, np.arange(1, 310), interval=20, blit=True)
Tk.mainloop()