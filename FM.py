#Imports
import tkinter as tk
from tkinter import ttk
import time, sys, math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

font_ = ('Arial', 14)
background_ = '#f5f5f5'
foreground_ = '#2c2f33'

root = tk.Tk()
root.configure(background = background_)
root.title('Модуляция')
#root.geometry('1920x1080')
root.resizable(1280, 720)

#style
style = ttk.Style()
style.theme_create('mod_theme', parent = 'alt', settings = {
    'TCombobox': {'configure':{
        'selectbackground': 'white',
        'fieldbackground': 'white',
        'selectforeground': foreground_
    }},
    'TLabel': {'configure':{
        'background': background_,
        'foreground': foreground_
    }}
})
style.theme_use("mod_theme")

def func(event=None):
    pass

#signal
def signal_freq_change(event=None):
    global s_frq
    s_frq = int(signal_freq.get())

def signal_amp_change(event=None):
    global s_amp, c_amp
    s_amp = int(signal_amp.get())

#carry
def carry_freq_change(event=None):
    global c_frq
    c_frq = int(carry_freq.get())

plot_container = tk.LabelFrame(root, text = '', height = 960, width = 1280, font = font_, bg = 'white')
plot_container.grid(row = 0, column = 0, rowspan = 9, padx = 5, pady = 5)
plot_container.configure(background = background_, foreground = foreground_)

#main label
type_text = tk.StringVar()
type_text.set('Частотная модуляция')
type_label = ttk.Label(plot_container, textvariable = type_text, font = font_, background = background_)
type_label.grid(row = 0, column = 0, sticky = ('N'), padx = 2, pady = 5)

#Signal frequency
signal_freq_lbl = ttk.Label(root, text = 'Частота (fc)', font = font_)
signal_freq_lbl.grid(row = 0, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
signal_freq = tk.IntVar()
signal_freq.set(2)
signal_freq_box = tk.Spinbox(root, from_ = 1, to = 100, textvariable = signal_freq, font = font_, foreground = foreground_, command = signal_freq_change)
signal_freq_box.grid(row = 0, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
signal_freq_box.bind('<Return>', func)

#Signal amplitude
signal_amp_lbl = ttk.Label(root, text = 'Амплитуда', font = font_)
signal_amp_lbl.grid(row = 1, column = 1, sticky = 'E', padx = (40, 5))
signal_amp = tk.IntVar()
signal_amp.set(25)
signal_amp_box = tk.Spinbox(root, from_ = 5, to = 95, textvariable = signal_amp, font = font_, foreground = foreground_, command = signal_amp_change, increment = 5.0)
signal_amp_box.grid(row = 1, column = 2, sticky = ('E', 'W'), padx = 2, pady = 5)
signal_amp_box.bind('<Return>', func)


#Carrying frequency
carry_freq_lbl = ttk.Label(root, text = 'Частота (fн)', font = font_)
carry_freq_lbl.grid(row = 3, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
carry_freq = tk.IntVar()
carry_freq.set(40)
carry_freq_box = tk.Spinbox(root, from_ = 10, to = 100, textvariable = carry_freq, font = font_, foreground = foreground_, command = carry_freq_change, increment = 5.0)
carry_freq_box.grid(row = 3, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
carry_freq_box.bind('<Return>', carry_freq_change)


deviation = tk.StringVar()
deviation_lbl = ttk.Label(root, text = 'Девиация', font = font_)
deviation_input = ttk.Entry(root, textvariable = deviation, font = font_)
deviation_lbl.place(x = 1270, y = 900)
deviation_input.place(x = 1380, y = 900)
deviation.set('6.0')

#variables
s_frq = int(signal_freq.get())
s_amp = int(signal_amp.get())

c_frq = int(carry_freq.get())
c_amp = 25
#c_width = int(carry_width.get())/100

#plotting
fig = plt.Figure(figsize=(12, 10))
x = np.arange(0, 10, 0.01)

def s_ani(i):
    s_line.set_ydata(np.sin((x-i/50.0)*s_frq)*s_amp)
    return s_line,

def c_ani(i):
    c_amp = signal_amp.get()
    c_line.set_ydata(np.sin((x-i/50.0)*c_frq)*c_amp)
    return c_line,

def m_ani(i):
    y_signal = np.sin((x-i/50.0)*s_frq)*s_amp
    dev = 6

    if not deviation.get().isalpha() and deviation.get() != '':
        dev = deviation.get().replace(',', '.')
        dev = float(dev)

    c_amp = signal_amp.get()
    y_carry = np.sin((x-i/50.0)*c_frq - dev*np.cos((x-i/50.0)*s_frq))*c_amp
    cm_line.set_ydata(y_carry)
    sm_line.set_ydata(y_signal)
    return cm_line, sm_line

def normalize(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(-100, 100)
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    #ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_label_coords(0.95, 0.45) 
    ax.set_xlabel('время')
    ax.set_ylabel('амплитуда')

canvas = FigureCanvasTkAgg(fig, master=plot_container)
canvas.get_tk_widget().grid(row=1,column=0)

s_ax = fig.add_subplot(311)
c_ax = fig.add_subplot(312)
m_ax = fig.add_subplot(313)
root.update()

y_signal = np.sin((x)*s_frq)*s_amp
y_max = max(y_signal)
y_carry = np.sin((x)*c_frq)*c_amp
s_line, = s_ax.plot(x, y_signal, 'k')
c_line, = c_ax.plot(x, y_carry)

y_signal = (np.sin((x)*s_frq)*s_amp)+y_max
y_max = max(y_signal)
y_carry = y_carry*(y_signal/y_max)
cm_line, = m_ax.plot(x, y_carry, 'r')
#spm_line, = m_ax.plot(x, y_signal, 'b', linewidth=2)
sm_line, = m_ax.plot(x, y_signal, 'k', linewidth=0.5)

s_ax.cla()
c_ax.cla()
m_ax.cla()

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)

s_ax.legend([s_line], ['Сигнал с fс'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание c fн'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line, sm_line], ['Частотно модулированный сигнал\n(модулированное по частоте колебание)', 'Сигнал с fс'], ncol = 3, loc = 'upper center', frameon=False)
#c_repeatable_point = int(250 * c_frq / 10)

a1 = animation.FuncAnimation(fig, s_ani, np.arange(1, 315), interval=20, blit=True)
a2 = animation.FuncAnimation(fig, c_ani, np.arange(1, 127), interval=20, blit=True)
a3 = animation.FuncAnimation(fig, m_ani, np.arange(1, 315), interval=20, blit=True)
root.mainloop()