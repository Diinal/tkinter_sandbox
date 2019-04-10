#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import time, gc
#---------End of imports

fig = plt.Figure()

x = np.arange(0, 10, 0.01)        # x-array

def disc_s_gen(i):
    #inc = int(i/1.5712)
    inc = i/20
    inc2 = int(5*i/np.pi)
    if 300-inc2 < -1000:
        inc2 -= 2000
    if 300-inc2 > 0:
        y_signal = signal.square((np.pi*x+inc + 0 )*1) + 1
        y_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc + np.pi)*1) + 1
    else:
        y_signal = signal.square((np.pi*x+inc + np.pi )*1) + 1
        y_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc + 0)*1) + 1
    return y_signal

def animate1(i):
    y_signal = disc_s_gen(i)
    line.set_ydata(y_signal)
    return line,

def animate2(i):
    inc = i/10
    #line2.set_ydata(np.sin((x+i/50.0)*c_frq)*c_amp)prev = 0
    y_carry = np.sin((np.pi*x+inc)*c_frq)*c_amp
    line2.set_ydata(y_carry)
    return line2,

def animate3(i):
    inc = i/10
    inc2 = int(10*i/np.pi)
    y_signal = disc_s_gen(i)
    y_carry = np.sin((np.pi*x+inc)*c_frq)*c_amp*(y_signal/2)
    line3.set_ydata(y_carry)
   # line3.set_ydata(y_carry)
    line4.set_ydata(y_signal)
    return line3, line4,

def average(y_mod):
    s, counter, prev = 0, 0, 0
    flag = False
    for i, a in enumerate(y_mod):
        if a > 0:
            flag = True
            s += a
            counter += 1
        else:
            if flag:
                y_mod[prev:i] = s/counter
                s, counter = 0, 0
                flag = False
            prev = i+1 
    return y_mod

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
frame = Tk.Frame(root)
frame.grid(row = 1, column = 0)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0,row=0)

ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
root.update()

c_frq = 2
c_amp = 2
line, = ax.plot(x, np.sin(x))
max_signal_amp = max(np.sin(x))
line2, = ax2.plot(x, np.sin(x*c_frq)*c_amp)

y_max = max(np.sin(x)+1)
y_signal = np.sin(x) 
y_carry = np.sin(x*c_frq + y_signal*5)*c_amp
line3, = ax3.plot(x, y_carry)
line4, = ax3.plot(x, y_signal)

ax.cla()
ax2.cla()
ax3.cla()
normalize(ax)
normalize(ax2)
normalize(ax3)

#ax.legend([line], ['san'])
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
ani1 = animation.FuncAnimation(fig, animate1, np.arange(1, 629), interval=20, blit=True)
ani2 = animation.FuncAnimation(fig, animate2, np.arange(1, 127), interval=20, blit=True) #if speed = 10.0 => range = 125, interval =20
ani3 = animation.FuncAnimation(fig, animate3, np.arange(1, 629), interval=20, blit=True)

Tk.mainloop()