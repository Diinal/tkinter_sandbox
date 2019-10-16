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
background_ = 'white'#'#f5f5f5'
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
    global s_amp, c_amp, carry_amp
    s_amp = int(signal_amp.get())
    carry_amp.set(s_amp*2)
    c_amp = s_amp*2

#carry
def carry_freq_change(event=None):
    global c_frq
    c_frq = int(carry_freq.get())

def scale_up(event=None):
    prev = signal_lvl.get()
    signal_lvl.set(prev+1)

def scale_down(event=None):
    prev = signal_lvl.get()
    signal_lvl.set(prev-1)

plot_width = 660
plot_height = 400

plot_container_signal = tk.LabelFrame(root, text = 'Сигнал', height = plot_height, width = plot_width, font = font_, bg = 'white')
plot_container_signal.grid(row = 0, column = 0, rowspan = 1, padx = (60, 10), pady = 20)
plot_container_signal.configure(background = background_, foreground = foreground_)

modulator_picture = tk.Canvas(root, width = 400, height = 386, bg = background_)
modulator_picture.grid(row = 0, column = 1, rowspan = 1, columnspan = 2, padx = 10, pady = 20, sticky = 'S')
modulator_picture.create_rectangle(2, 2, 400, 386, outline = 'black', width = 4)
modulator_picture.create_line(30, 386, 200, 2, width = 4, smooth = 1)
modulator_picture.create_line(200, 2, 370, 386, width = 4, smooth = 1)

plot_container_modulation = tk.LabelFrame(root, text = 'Амплитудно модулированный сигнал', height = plot_height, width = 900, font = font_, bg = 'white')
plot_container_modulation.grid(row = 0, column = 3, rowspan = 1, padx = 10, pady = 20, sticky = ('W'))
plot_container_modulation.configure(background = background_, foreground = foreground_)

plot_container_settings = tk.LabelFrame(root, text = 'Настройки', height = plot_height, width = plot_width, font = font_, bg = 'white')
plot_container_settings.grid(row = 1, column = 0, columnspan = 1, padx = (60, 10), pady = 20, sticky = ('N','W','S','E'))
plot_container_settings.configure(background = background_, foreground = foreground_)

signal_settings = tk.LabelFrame(plot_container_settings, text = 'Сигнал:', height = plot_height//2, width = plot_width, font = font_, bg = 'white')
signal_settings.grid(row = 0, column = 0, padx = (20, 5), pady = 20)
signal_settings.configure(background = background_, foreground = foreground_)

carry_settings = tk.LabelFrame(plot_container_settings, text = 'Несущее колебание:', height = plot_height//2, width = plot_width, font = font_, bg = 'white')
carry_settings.grid(row = 1, column = 0, padx = (20, 5), pady = 20)
carry_settings.configure(background = background_, foreground = foreground_)

plot_container_carry = tk.LabelFrame(root, text = 'Несущее колебание', height = plot_height, width = plot_width, font = font_, bg = 'white')
plot_container_carry.grid(row = 1, column = 2, columnspan = 2, rowspan = 1, padx = 10, pady = 20, sticky = ('W'))
plot_container_carry.configure(background = background_, foreground = foreground_)

#vert scale
signal_lvl = tk.IntVar()
signal_scale = tk.Scale(root, from_ = 100, to = -100, bg = 'white', length = 300, variable = signal_lvl)
signal_scale.place(x = 5, y = 100)
signal_lvl.set(25)

up_button = tk.Button(root, text = '+', command = scale_up, font = font_, bg = 'white', width = 2)
up_button.place(x = 5, y = 60)

down_button = tk.Button(root, text = '-', command = scale_down, font = font_, bg = 'white', width = 2)
down_button.place(x = 5, y = 405)

#Signal frequency
#signal_freq_lbl = ttk.Label(plot_container_settings, text = 'Сигнал:', font = font_)
#signal_freq_lbl.grid(row = 0, column = 1, sticky = ('E', 'S'), padx = (5, 5), pady = 5)
signal_freq_lbl = ttk.Label(signal_settings, text = 'Частота (f c)', font = font_)
signal_freq_lbl.grid(row = 1, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 15)
signal_freq = tk.IntVar()
signal_freq.set(2)
signal_freq_box = tk.Spinbox(signal_settings, from_ = 1, to = 100, textvariable = signal_freq, font = font_, foreground = foreground_, command = signal_freq_change)
signal_freq_box.grid(row = 1, column = 2, sticky = ('E', 'W', 'S'), padx = (2, 15), pady = 15)
signal_freq_box.bind('<Return>', func)

#Signal amplitude
signal_amp_lbl = ttk.Label(signal_settings, text = 'Амплитуда', font = font_)
signal_amp_lbl.grid(row = 2, column = 1, sticky = 'E', padx = (40, 5), pady = 15)
signal_amp = tk.IntVar()
signal_amp.set(25)
signal_amp_box = tk.Spinbox(signal_settings, from_ = 5, to = 95, textvariable = signal_amp, font = font_, foreground = foreground_, command = signal_amp_change, increment = 5.0)
signal_amp_box.grid(row = 2, column = 2, sticky = ('E', 'W'), padx = (2, 15), pady = 15)
signal_amp_box.bind('<Return>', func)

#Carrying frequency
#signal_freq_lbl = ttk.Label(plot_container_settings, text = 'Несущее колебание:', font = font_)
#signal_freq_lbl.grid(row = 3, column = 1, sticky = ('E', 'S'), padx = (5, 5), pady = (30, 5))
carry_freq_lbl = ttk.Label(carry_settings, text = 'Частота (f н)', font = font_)
carry_freq_lbl.grid(row = 4, column = 1, sticky = ('E', 'S'), padx = (65, 5), pady = 15)
carry_freq = tk.IntVar()
carry_freq.set(40)
carry_freq_box = tk.Spinbox(carry_settings, from_ = 10, to = 100, textvariable = carry_freq, font = font_, foreground = foreground_, command = carry_freq_change, increment = 5.0)
carry_freq_box.grid(row = 4, column = 2, sticky = ('E', 'W', 'S'), padx = (2, 15), pady = 15)
carry_freq_box.bind('<Return>', carry_freq_change)

carry_amp = tk.IntVar()
carry_amp.set(50)

# root.update_idletasks() 
def configure(event):
    width = root.winfo_width()
    height = root.winfo_height()
    print(width, height)
#root.bind("<Configure>", configure)


#variables
s_frq = int(signal_freq.get())
s_amp = int(signal_amp.get())

c_frq = int(carry_freq.get())
c_amp = int(carry_amp.get())

#plotting
def s_ani(i):
    if (max(np.sin((x-i/50.0)*s_frq)*s_amp) + signal_lvl.get()) < 99 and (min(np.sin((x+i/50.0)*s_frq)*s_amp) + signal_lvl.get()) > -99:
        s_line.set_ydata(np.sin((x-i/50.0)*s_frq)*s_amp + signal_lvl.get())
    elif signal_lvl.get() > 0:
        s_line.set_ydata(np.sin((x-i/50.0)*s_frq)*s_amp + 99 - s_amp)
    else:
        s_line.set_ydata(np.sin((x-i/50.0)*s_frq)*s_amp - 99 + s_amp)
    return s_line,

def c_ani(i):
    c_line.set_ydata(np.sin((x-i/50.0)*c_frq)*c_amp)
    return c_line,

def m_ani(i):
    y_envelope_up = (np.sin((x-i/50.0)*s_frq)*s_amp)
    y_envelope_down = (np.sin((x-i/50.0)*s_frq+np.pi)*s_amp)

    if (max(y_envelope_up) + signal_lvl.get()) < 99 and (min(y_envelope_up) + signal_lvl.get()) > -99:
        y_envelope_up = y_envelope_up + signal_lvl.get()
        y_envelope_down = y_envelope_down - signal_lvl.get()
    elif signal_lvl.get() > 0:
        y_envelope_up = y_envelope_up + 99 - s_amp
        y_envelope_down = y_envelope_down - 99 + s_amp
    else:
        y_envelope_up = y_envelope_up - 99 + s_amp
        y_envelope_down = y_envelope_down + 99 - s_amp
    
    cm_line.set_ydata(np.sin((x-i/50.0)*c_frq)*c_amp*(y_envelope_up/(s_amp*2)))
    sm_line.set_ydata(y_envelope_up)
    #sm_line.set_color('red')
    spm_line.set_ydata(y_envelope_down)
    #subsignal_label.set_text('Сигнал')

    return cm_line, sm_line, spm_line#, subsignal_label

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

x = np.arange(0, 10, 0.01)

fig_signal = plt.Figure(figsize=(6.6 , 4), dpi = 100)
canvas_signal = FigureCanvasTkAgg(fig_signal, master = plot_container_signal)
canvas_signal.get_tk_widget().grid(row = 0, column = 0)

fig_modulation = plt.Figure(figsize=(6.6 , 4), dpi = 100)
canvas_modulation = FigureCanvasTkAgg(fig_modulation, master = plot_container_modulation)
canvas_modulation.get_tk_widget().grid(row = 1, column = 0)

fig_carry = plt.Figure(figsize=(9 , 4), dpi = 100)
canvas_carry = FigureCanvasTkAgg(fig_carry, master = plot_container_carry)
canvas_carry.get_tk_widget().grid(row = 1, column = 0)

s_ax = fig_signal.add_subplot(111)
c_ax = fig_carry.add_subplot(111)
m_ax = fig_modulation.add_subplot(111)

root.update()

y_signal = np.sin((x)*s_frq)*s_amp
y_max = max(y_signal)
y_carry = np.sin((x)*c_frq)*c_amp
s_line, = s_ax.plot(x, y_signal, 'k')
c_line, = c_ax.plot(x, y_carry)

y_signal = (np.sin((x)*s_frq)*s_amp)+y_max
y_max = max(y_signal)
y_carry = y_carry*(y_signal/y_max)
cm_line, = m_ax.plot(x, y_carry, 'g')
spm_line, = m_ax.plot(x, y_signal, 'b', linewidth=2)
sm_line, = m_ax.plot(x, y_signal, 'r', linewidth=2)

s_ax.cla()
c_ax.cla()
m_ax.cla()

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)

s_ax.legend([s_line], ['Сигнал с fс'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание c fн'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line], ['Амплитудно модулированный сигнал\n(модулированное по амплитуде колебание)'], loc = 'upper center', frameon=False)
fig_modulation.legend([sm_line, spm_line], ['Верхняя огибающая', 'Нижняя огибающая'], loc = 'lower center', frameon=False, ncol=2)
#subsignal_label = m_ax.text(0.87, 0.93, 'lkj', transform=m_ax.transAxes)


a1 = animation.FuncAnimation(fig_signal, s_ani, np.arange(1, 315), interval=20, blit=True)
a2 = animation.FuncAnimation(fig_carry, c_ani, np.arange(1, 127), interval=20, blit=True)
a3 = animation.FuncAnimation(fig_modulation, m_ani, np.arange(1, 315), interval=20, blit=True)

root.mainloop()