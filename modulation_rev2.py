#Imports
import tkinter as tk
from tkinter import ttk
import time, sys, math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#TODO
# create new gui without notebook with embeded matplotlib+
# create function for changable variables+

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
    if type_modulation.current() == 0:
        carry_amp.set(s_amp*2)
        c_amp = s_amp*2

def signal_phase_change(event=None):
    global s_phs
    s_phs = int(signal_phase.get())

#carry
def carry_freq_change(event=None):
    global c_frq
    c_frq = int(carry_freq.get())

def carry_amp_change(event=None):
    global c_amp
    c_amp = int(carry_amp.get())

def carry_phase_change(event=None):
    global c_phs
    c_phs = int(carry_phase.get())


def change_modulation(event=None):
    global deviation_lbl
    global deviation_input
    if type_modulation.current() == 0:
        carry_amp_box.configure(state = 'disable' )
        #deviation_lbl.grid_remove()
        #deviation_input.grid_remove()
        deviation_lbl.place_forget()
        deviation_input.place_forget()

    elif type_modulation.current() == 1:
        carry_amp_box.configure(state = 'normal' )
        #deviation_lbl.grid(row = 7, column = 1, sticky = ('E'), padx = (40, 5), pady = 5)
        #deviation_input.grid(row = 7, column = 2, sticky = ('E', 'W'), padx = 2, pady = 5)
        deviation_lbl.place(x = 1300, y = 900)
        deviation_input.place(x = 1425, y = 900)
    elif type_modulation.current() == 2:
        carry_amp_box.configure(state = 'normal')
        deviation_lbl.place(x = 1300, y = 900)
        deviation_input.place(x = 1425, y = 900)

plot_container = tk.LabelFrame(root, text = 'Амплитудная модуляция', height = 960, width = 1280, font = font_)
plot_container.grid(row = 0, column = 0, rowspan = 9, padx = 5, pady = 5)
plot_container.configure(background = background_, foreground = foreground_)

#Signal frequency
signal_freq_lbl = ttk.Label(root, text = 'Частота', font = font_)
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
signal_amp_box = tk.Spinbox(root, from_ = 5, to = 300, textvariable = signal_amp, font = font_, foreground = foreground_, command = signal_amp_change, increment = 5.0)
signal_amp_box.grid(row = 1, column = 2, sticky = ('E', 'W'), padx = 2, pady = 5)
signal_amp_box.bind('<Return>', func)

#Signal phase
signal_phase_lbl = ttk.Label(root, text = 'Фаза', font = font_)
signal_phase_lbl.grid(row = 2, column = 1, sticky = ('E', 'N'), padx = (40, 5), pady = 5)
signal_phase = tk.IntVar()
signal_phase.set(0)
signal_phase_box = tk.Spinbox(root, from_ = 0, to = 100, textvariable = signal_phase, font = font_, foreground = foreground_, command = signal_phase_change, increment = 5.0)
signal_phase_box.grid(row = 2, column = 2, sticky = ('E', 'W', 'N'), padx = 2, pady = 5)
signal_phase_box.bind('<Return>', func)


#Carrying frequency
carry_freq_lbl = ttk.Label(root, text = 'Частота', font = font_)
carry_freq_lbl.grid(row = 3, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
carry_freq = tk.IntVar()
carry_freq.set(40)
carry_freq_box = tk.Spinbox(root, from_ = 10, to = 100, textvariable = carry_freq, font = font_, foreground = foreground_, command = carry_freq_change, increment = 5.0)
carry_freq_box.grid(row = 3, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
carry_freq_box.bind('<Return>', carry_freq_change)

#Carrying amplitude
carry_amp_lbl = ttk.Label(root, text = 'Амплитуда', font = font_)
carry_amp_lbl.grid(row = 4, column = 1, sticky = ('E'), padx = (40, 5), pady = 5)
carry_amp = tk.IntVar()
carry_amp.set(50)
carry_amp_box = tk.Spinbox(root, from_ = 5, to = 300, textvariable = carry_amp, font = font_, foreground = foreground_, command = carry_amp_change, increment = 5.0, state = 'disable')
carry_amp_box.grid(row = 4, column = 2, sticky = ('E', 'W'), padx = 2, pady = 5)
carry_amp_box.bind('<Return>', func)

#Carrying phase
carry_phase_lbl = ttk.Label(root, text = 'Фаза', font = font_)
carry_phase_lbl.grid(row = 5, column = 1, sticky = ('E', 'N'), padx = (40, 5), pady = 5)
carry_phase = tk.IntVar()
carry_phase.set(0)
carry_phase_box = tk.Spinbox(root, from_ = 0, to = 100, textvariable = carry_phase, font = font_, foreground = foreground_, command = carry_phase_change, increment = 5.0)
carry_phase_box.grid(row = 5, column = 2, sticky = ('E', 'W', 'N'), padx = 2, pady = 5)
carry_phase_box.bind('<Return>', func)


#Type of modulation switcher
type_m_lbl = ttk.Label(root, text = 'Тип модуляции:', font = font_)
type_m_lbl.grid(row = 6, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
type_m = tk.StringVar()
type_modulation = ttk.Combobox(root, state = 'readonly', textvariable = type_m , font = font_)
type_modulation.grid(row = 6, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
type_modulation['values'] = ('Амплитудная', 'Частотная', 'Фазовая')
type_modulation.current(0)
root.option_add('*TCombobox*Listbox.font', font_)
type_modulation.bind('<<ComboboxSelected>>', change_modulation)

deviation = tk.StringVar()
deviation_lbl = ttk.Label(root, text = 'Девиация', font = font_)
deviation_input = ttk.Entry(root, textvariable = deviation, font = font_)


#variables
s_frq = int(signal_freq.get())
s_amp = int(signal_amp.get())
s_phs = int(signal_phase.get())

c_frq = int(carry_freq.get())
c_amp = int(carry_amp.get())
c_phs = int(carry_phase.get())

#plotting
fig = plt.Figure(figsize=(12, 10))
x = np.arange(0, 10, 0.01)

def s_ani(i):
    s_line.set_ydata(np.sin((x+s_phs+i/50.0)*s_frq)*s_amp)
    return s_line,

def c_ani(i):
    c_line.set_ydata(np.sin((x+c_phs+i/50.0)*c_frq)*c_amp)
    return c_line,

def m_ani(i):
    y_signal, y_carry, label = calc_mod_ani(i)
    cm_line.set_ydata(y_carry)
    sm_line.set_ydata(y_signal)
    subsignal_label.set_text(label)
    return cm_line, sm_line, subsignal_label

def calc_mod_ani(i):
    if type_modulation.current() == 0:
        y_signal = np.sin((x+s_phs+i/50.0)*s_frq)*s_amp
        y_max = max(y_signal)
        y_signal = (np.sin((x+s_phs+i/50.0)*s_frq)*s_amp)+y_max
        y_max = max(y_signal)
        y_carry = np.sin((x+c_phs+i/50.0)*c_frq)*c_amp*(y_signal/y_max)
        label = 'Сигнал'
        return y_signal, y_carry, label

    elif type_modulation.current() == 1:
        y_signal = np.sin((x+s_phs+i/50.0)*s_frq)*s_amp
        y_max = max(y_signal)
        #dev = 14/y_max
        dev = 1
        if not deviation.get().isalpha() and deviation.get() != '':
            dev = float(deviation.get())
        y_carry = np.sin((x+c_phs+i/50.0)*c_frq - dev*np.cos((x+s_phs+i/50.0)*s_frq))*c_amp
        label = 'Сигнал'
        return y_signal, y_carry, label

    elif type_modulation.current() == 2:
        dev = 0.1
        y_signal = np.sin((x+s_phs+i/50.0)*s_frq)*s_amp
        if not deviation.get().isalpha() and deviation.get() != '':
            dev = float(deviation.get())
        y_old_carry = np.sin((x+c_phs+i/50.0)*c_frq)*c_amp
        y_carry = np.sin((x+c_phs+i/50.0)*c_frq - dev*y_signal)*c_amp
        label = 'Несущее колебание'
        return y_old_carry, y_carry, label
        

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
canvas.get_tk_widget().grid(row=0,column=0)

s_ax = fig.add_subplot(311)
c_ax = fig.add_subplot(312)
m_ax = fig.add_subplot(313)
root.update()

y_signal = np.sin((x+s_phs)*s_frq)*s_amp
y_max = max(y_signal)
y_carry = np.sin((x+c_phs)*c_frq)*c_amp
s_line, = s_ax.plot(x, y_signal, 'r')
c_line, = c_ax.plot(x, y_carry)

y_signal = (np.sin((x+s_phs)*s_frq)*s_amp)+y_max
y_max = max(y_signal)
y_carry = y_carry*(y_signal/y_max)
cm_line, = m_ax.plot(x, y_carry)
sm_line, = m_ax.plot(x, y_signal, 'r')

s_ax.cla()
c_ax.cla()
m_ax.cla()

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)

s_ax.legend([s_line], ['Сигнал'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line, sm_line], ['Модулированное несущее колебание', ' '], loc = 'upper center', frameon=False, ncol=2)
subsignal_label = m_ax.text(0.7, 0.90, '', transform=m_ax.transAxes)
#c_repeatable_point = int(250 * c_frq / 10)

a1 = animation.FuncAnimation(fig, s_ani, np.arange(1, 315), interval=20, blit=True)
a2 = animation.FuncAnimation(fig, c_ani, np.arange(1, 127), interval=20, blit=True)
a3 = animation.FuncAnimation(fig, m_ani, np.arange(1, 315), interval=20, blit=True)
root.mainloop()