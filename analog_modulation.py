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
    global s_amp, c_amp, carry_amp
    s_amp = int(signal_amp.get())
    if type_modulation.current() == 0:
        carry_amp.set(s_amp*2)
        c_amp = s_amp*2
    elif type_modulation.current() >= 2:
        carry_amp.set(s_amp)
        c_amp = s_amp

#carry
def carry_freq_change(event=None):
    global c_frq
    c_frq = int(carry_freq.get())

def carry_amp_change(event=None):
    global c_amp
    c_amp = int(carry_amp.get())

def carry_width_change(event = None):
    global c_width
    c_width = int(carry_width.get())/100

def change_modulation(event=None):
    global deviation_lbl
    global deviation_input
    global s_amp, c_amp, carry_amp

    types = ['Амплитудная модуляция', 'Частотная модуляция', 'Фазовая модуляция']

    type_text.set(types[type_modulation.current()])

    # FIXME BUG 18.08.2019 state = 'disable' don't remove when type of modulation is changed
    if type_modulation.current() == 0:
        carry_amp.set(s_amp*2)
        c_amp = s_amp*2
        carry_amp_box.configure( state = 'disable' )
        signal_scale.configure( state = 'active' )
        up_button.configure( state = 'active' )
        down_button.configure( state = 'active' )
        deviation_lbl.place_forget()
        deviation_input.place_forget()
        carry_width_lbl.place_forget()
        carry_width_box.place_forget()
        carry_width_percent_lbl.place_forget()
        white_label.place_forget()

    elif type_modulation.current() == 1:
        # carry_freq.set(40)
        deviation.set(5)
        carry_amp.set(s_amp)
        c_amp = s_amp
        carry_amp_box.configure( state = 'disable' )
        signal_scale.configure( state = 'disable' )
        up_button.configure( state = 'disable' )
        down_button.configure( state = 'disable' )
        deviation_lbl.place(x = 1270, y = 900)
        deviation_input.place(x = 1380, y = 900)
        carry_width_lbl.place_forget()
        carry_width_box.place_forget()
        carry_width_percent_lbl.place_forget()
        white_label.place(x = 750, y = 710)

    elif type_modulation.current() == 2:
        # carry_freq.set(15)
        deviation.set(1)
        carry_amp.set(s_amp)
        c_amp = s_amp
        carry_amp_box.configure( state = 'disable' )
        signal_scale.configure( state = 'disable' )
        up_button.configure( state = 'disable' )
        down_button.configure( state = 'disable' )
        deviation_lbl.place(x = 1270, y = 900)
        deviation_input.place(x = 1380, y = 900)
        carry_width_lbl.place_forget()
        carry_width_box.place_forget()
        carry_width_percent_lbl.place_forget()
        white_label.place_forget()

def scale_up(event=None):
    prev = signal_lvl.get()
    signal_lvl.set(prev+1)

def scale_down(event=None):
    prev = signal_lvl.get()
    signal_lvl.set(prev-1)

plot_container = tk.LabelFrame(root, text = '', height = 960, width = 1280, font = font_, bg = 'white')
plot_container.grid(row = 0, column = 0, rowspan = 9, padx = 5, pady = 5)
plot_container.configure(background = background_, foreground = foreground_)

#main label
type_text = tk.StringVar()
type_text.set('Амплитудная модуляция')
type_label = ttk.Label(plot_container, textvariable = type_text, font = font_, background = background_)
type_label.grid(row = 0, column = 0, sticky = ('N'), padx = 2, pady = 5)

#vert scale
signal_lvl = tk.IntVar()
signal_scale = tk.Scale(root, from_ = 100, to = -100, bg = 'white', length = 250, variable = signal_lvl)
signal_scale.place(x = 25, y = 140)
signal_lvl.set(25)

up_button = tk.Button(root, text = '+', command = scale_up, font = font_, bg = 'white', width = 2)
up_button.place(x = 25, y = 100)

down_button = tk.Button(root, text = '-', command = scale_down, font = font_, bg = 'white', width = 2)
down_button.place(x = 25, y = 395)

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
carry_freq.set(20)
carry_freq_box = tk.Spinbox(root, from_ = 10, to = 100, textvariable = carry_freq, font = font_, foreground = foreground_, command = carry_freq_change, increment = 5.0)
carry_freq_box.grid(row = 3, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
carry_freq_box.bind('<Return>', carry_freq_change)

#Carrying amplitude
carry_amp_lbl = ttk.Label(root, text = 'Амплитуда', font = font_)
carry_amp_lbl.grid(row = 4, column = 1, sticky = ('E'), padx = (40, 5), pady = 5)
carry_amp = tk.IntVar()
carry_amp.set(50)
carry_amp_box = tk.Spinbox(root, from_ = 5, to = 100, textvariable = carry_amp, font = font_, foreground = foreground_, command = carry_amp_change, increment = 5.0, state = 'disable')
carry_amp_box.grid(row = 4, column = 2, sticky = ('E', 'W'), padx = 2, pady = 5)
carry_amp_box.bind('<Return>', func)

#Carrying impulse width
carry_width_lbl = ttk.Label(root, text = 'Ширина', font = font_)
carry_width_percent_lbl = ttk.Label(root, text = '%', font = font_)
carry_width = tk.IntVar()
carry_width_box = tk.Spinbox(root, from_ = 1, to = 100, textvariable = carry_width, font = font_, foreground = foreground_, command = carry_width_change, increment = 5.0, width = 5)
carry_width.set(50)

#Type of modulation switcher
type_m_lbl = ttk.Label(root, text = 'Тип:', font = font_)
type_m_lbl.grid(row = 6, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
type_m = tk.StringVar()
type_modulation = ttk.Combobox(root, state = 'readonly', textvariable = type_m , font = font_)
type_modulation.grid(row = 6, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
type_modulation['values'] = ('АМ', 'ЧМ', 'ФМ')
type_modulation.current(0)
root.option_add('*TCombobox*Listbox.font', font_)
type_modulation.bind('<<ComboboxSelected>>', change_modulation)

deviation = tk.StringVar()
deviation_lbl = ttk.Label(root, text = 'Девиация', font = font_)
deviation_input = ttk.Entry(root, textvariable = deviation, font = font_)

white_label = ttk.Label(root, text = '             ', font = font_, background = 'white')


#variables
s_frq = int(signal_freq.get())
s_amp = int(signal_amp.get())

c_frq = int(carry_freq.get())
c_amp = int(carry_amp.get())
c_width = int(carry_width.get())/100

#plotting
fig = plt.Figure(figsize=(12, 10))
x = np.arange(0, 10, 0.01)

def s_ani(i):
    y_signal, y_carry, label_up, label_down, label, y_envelope_down = calc_mod_ani(i)
    s_line.set_ydata(y_signal)
    return s_line,

def c_ani(i):
    if type_modulation.current() <= 2:
        c_line.set_ydata(np.sin((x+i/50.0)*c_frq)*c_amp)
    else:
        y_carry = signal.square((x+i/50.0)*c_frq, duty=c_width)*c_amp
        y_max = max(y_carry)
        c_line.set_ydata(y_carry+y_max)
    return c_line,

def m_ani(i):
    y_signal, y_carry, label_up, label_down, label, y_envelope_down = calc_mod_ani(i)
    cm_line.set_ydata(y_carry)
    sm_line.set_ydata(y_signal)
    spm_line.set_ydata(y_envelope_down)
    if type_modulation.current() == 2:
        sm_line.set_ydata(np.sin((x+i/50.0)*s_frq)*s_amp)
        sm_line.set( linewidth = 0.75 )
        subsignal_label_down.set_y(0.85)
    elif type_modulation.current() == 1:
        sm_line.set_ydata(np.sin((x+i/50.0)*s_frq)*s_amp)
        sm_line.set(linewidth = 0.75 )

    subsignal_label_up.set_text(label_up)
    subsignal_label_down.set_text(label_down)
    signal_label.set_text(label)

    return cm_line, sm_line, spm_line, subsignal_label_up, subsignal_label_down, signal_label

def calc_mod_ani(i):
    #AM
    if type_modulation.current() == 0:
        y_signal = np.sin((x+i/50.0)*s_frq)*s_amp
        y_envelope_down = (np.sin((x+i/50.0)*s_frq+np.pi)*s_amp)

        if (max(y_signal) + signal_lvl.get()) < 99 and (min(y_signal) + signal_lvl.get()) > -99:
            y_signal = y_signal + signal_lvl.get()
            y_envelope_down = y_envelope_down - signal_lvl.get()
        elif signal_lvl.get() > 0:
             y_signal = y_signal + 99 - s_amp
             y_envelope_down = y_envelope_down - 99 + s_amp
        else:
             y_signal = y_signal - 99 + s_amp
             y_envelope_down = y_envelope_down + 99 - s_amp

        y_carry = np.sin((x+i/50.0)*c_frq)*c_amp*(y_signal/(s_amp*2))
        label = 'Амплитудно модулированный сигнал\n(модулированное по амплитуде колебание)'
        label_up = 'Верхняя огибающая'
        label_down = 'Нижняя огибающая'
        spm_line.set_color('b')
        return y_signal, y_carry, label_up, label_down, label, y_envelope_down

    #FM
    elif type_modulation.current() == 1:
        y_signal = np.sin((x+i/50.0)*s_frq)*s_amp
        #dev = 14/y_max
        dev = 1
        if not deviation.get().isalpha() and deviation.get() != '':
            dev = deviation.get().replace(',', '.')
            dev = float(dev)
        y_carry = np.sin((x+i/50.0)*c_frq - dev*np.cos((x+i/50.0)*s_frq))*c_amp
        label = 'Частотно модулированный сигнал\n(модулированное по частоте колебание)'
        label_up = 'Сигнал с fc'
        label_down = ' '
        spm_line.set_color('k')
        return y_signal, y_carry, label_up, label_down, label, 0

    #PM
    elif type_modulation.current() == 2:
        dev = 0.1
        y_signal = np.sin((x+i/50.0)*s_frq)*s_amp
        if not deviation.get().isalpha() and deviation.get() != '':
            dev = deviation.get().replace(',', '.')
            dev = float(dev)/10
        y_old_carry = np.sin((x+i/50.0)*c_frq)*c_amp
        y_carry = np.sin((x+i/50.0)*c_frq - dev*y_signal)*c_amp
        label = 'Фазово модулированный сигнал\n(модулированное по фазе колебание)'
        label_up = 'Сигнал'
        label_down = 'Старое несущее\nколебание'
        spm_line.set_color('#1f77b4')
        spm_line.set(linewidth = 0.75)
        return y_signal, y_carry, label_up, label_down, label, y_old_carry

    
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
cm_line, = m_ax.plot(x, y_carry, 'k')
spm_line, = m_ax.plot(x, y_signal, 'b', linewidth=2)
sm_line, = m_ax.plot(x, y_signal, 'r', linewidth=2)

s_ax.cla()
c_ax.cla()
m_ax.cla()

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)

s_ax.legend([s_line], ['Сигнал с fc'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание с fн'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line, sm_line, spm_line], ['                                                                       ', '                                      ', ' '], loc = 'upper left', frameon=False, ncol=3)
signal_label = m_ax.text(0.06, 0.85, '', transform=m_ax.transAxes)
subsignal_label_up = m_ax.text(0.46, 0.90, '', transform=m_ax.transAxes)
subsignal_label_down = m_ax.text(0.71, 0.90, '', transform=m_ax.transAxes)
#c_repeatable_point = int(250 * c_frq / 10)

a1 = animation.FuncAnimation(fig, s_ani, np.arange(1, 315), interval=20, blit=True)
a2 = animation.FuncAnimation(fig, c_ani, np.arange(1, 127), interval=20, blit=True)
a3 = animation.FuncAnimation(fig, m_ani, np.arange(1, 315), interval=20, blit=True)
root.mainloop()