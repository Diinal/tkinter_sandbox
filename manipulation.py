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
root.title('Манипуляция')
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


#carry
def carry_freq_change(event=None):
    global c_frq
    c_frq = int(carry_freq.get())

def carry_amp_change(event=None):
    global c_amp
    c_amp = int(carry_amp.get())

def change_manipulation(event = None):
    types = ['Амплитудная манипуляция (телеграфия)', 'Частотная манипуляция (телеграфия)', 'Фазовая манипуляция (телеграфия)', 'Относительно-фазовая манипуляция (телеграфия)',]
    type_text.set(types[type_manipulation.current()])
    if type_manipulation.current() == 0:
        pass

plot_container = tk.LabelFrame(root, text = '', height = 960, width = 1280, font = font_)
plot_container.grid(row = 0, column = 0, rowspan = 9, padx = 5, pady = 5)
plot_container.configure(background = background_, foreground = foreground_)

#main label
type_text = tk.StringVar()
type_text.set('Амплитудная манипуляция')
type_label = ttk.Label(plot_container, textvariable = type_text, font = font_, background = background_)
type_label.grid(row = 0, column = 0, sticky = ('N'), padx = 2, pady = 5)

#Signal parameters
#NOT TODAY!!!

#Carrying frequency
carry_freq_lbl = ttk.Label(root, text = 'Частота', font = font_)
carry_freq_lbl.grid(row = 3, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
carry_freq = tk.IntVar()
carry_freq.set(10)
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
#carry_amp_box.bind('<Return>', func)

#Type of modulation switcher
type_m_lbl = ttk.Label(root, text = 'Тип:', font = font_)
type_m_lbl.grid(row = 6, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)
type_m = tk.StringVar()
type_manipulation = ttk.Combobox(root, state = 'readonly', textvariable = type_m , font = font_)
type_manipulation.grid(row = 6, column = 2, sticky = ('E', 'W', 'S'), padx = 2, pady = 5)
type_manipulation['values'] = ('АМт', 'ЧМт', 'ФМт', 'ОФМт')
type_manipulation.current(0)
root.option_add('*TCombobox*Listbox.font', font_)
type_manipulation.bind('<<ComboboxSelected>>', change_manipulation)

#variables
s_amp = 25

c_frq = int(carry_freq.get())
c_amp = int(carry_amp.get())

#plotting
fig = plt.Figure(figsize=(12, 10))
x = np.arange(0, 10, 0.01)

def discr_signal_gen(i):
    global bit_0
    #inc = int(i/1.5712)
    inc = i/20
    inc2 = int(5*i/np.pi)
    #inc2 = int(2*i)
    if 300-inc2 < -1000:
        inc2 -= 2000
    if 300-inc2 > 0:
        y_signal = signal.square((np.pi*x+inc + 0 )*1)*s_amp + s_amp
        y_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc + np.pi)*1)*s_amp + s_amp
    else:
        y_signal = signal.square((np.pi*x+inc + np.pi )*1)*s_amp + s_amp
        y_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc + 0)*1)*s_amp + s_amp
    return y_signal

def s_ani(i):
    inc2 = int(5*i/np.pi)
    y_signal = discr_signal_gen(i)
    s_line.set_ydata(y_signal)

    
    bit_0.set_x((1 - 0.965 - inc2/1000)%1)
    bit_0.set_text(str(1 if y_signal[(1000-965-inc2)%1000]>0 else 0))

    bit_1.set_x((1 - 0.865 - inc2/1000)%1)
    bit_1.set_text(str(1 if y_signal[(1000-865-inc2)%1000]>0 else 0))

    bit_2.set_x((1 - 0.765 - inc2/1000)%1)
    bit_2.set_text(str(1 if y_signal[(1000-765-inc2)%1000]>0 else 0))

    bit_3.set_x((1 - 0.665 - inc2/1000)%1)
    bit_3.set_text(str(1 if y_signal[(1000-665-inc2)%1000]>0 else 0))

    bit_4.set_x((1 - 0.565 - inc2/1000)%1)
    bit_4.set_text(str(1 if y_signal[(1000-565-inc2)%1000]>0 else 0))

    bit_5.set_x((1 - 0.465 - inc2/1000)%1)
    bit_5.set_text(str(1 if y_signal[(1000-465-inc2)%1000]>0 else 0))

    bit_6.set_x((1 - 0.365 - inc2/1000)%1)
    bit_6.set_text(str(1 if y_signal[(1000-365-inc2)%1000]>0 else 0))

    bit_7.set_x((1 - 0.265 - inc2/1000)%1)
    bit_7.set_text(str(1 if y_signal[(1000-265-inc2)%1000]>0 else 0))

    bit_8.set_x((1 - 0.165 - inc2/1000)%1)
    bit_8.set_text(str(1 if y_signal[(1000-165-inc2)%1000]>0 else 0))

    bit_9.set_x((1 - 0.065 - inc2/1000)%1)
    bit_9.set_text(str(1 if y_signal[(1000-65-inc2)%1000]>0 else 0))

    return s_line, bit_0, bit_1, bit_2, bit_3, bit_4, bit_5, bit_6, bit_7, bit_8, bit_9

def c_ani(i):
    inc = i/(10*np.pi)
    inc = i/20
    c_line.set_ydata(np.sin((np.pi*x+inc)*c_frq/2)*c_amp)
    return c_line,

def m_ani(i):
    y_signal, y_carry = calc_mod_ani(i)
    cm_line.set_ydata(y_carry)
    sm_line.set_ydata(y_signal)
    return cm_line, sm_line,

def calc_mod_ani(i):
    inc = i/(10*np.pi)
    inc = i/20
    #ASK
    if type_manipulation.current() == 0:
        y_signal = discr_signal_gen(i)
        y_carry = np.sin((np.pi*x+inc)*c_frq/2)*c_amp*(y_signal/(2*s_amp))
        return y_signal, y_carry

    #FSK
    if type_manipulation.current() == 1:
        y_signal = discr_signal_gen(i)
        y_carry = np.sin((np.pi*x+inc)*(c_frq/2+8*(y_signal/(2*s_amp))))*c_amp
        return y_signal, y_carry
    #PSK
    if type_manipulation.current() == 2:
        y_signal = discr_signal_gen(i)
        y_carry = np.sin((np.pi*x+inc + np.pi*(y_signal/(2*s_amp)))*(c_frq/2))*c_amp
        return y_signal, y_carry
    #OPSK
    if type_manipulation.current() == 3:
        inc2 = int(5*i/np.pi)
        y_signal = discr_signal_gen(i)
        if 300-inc2 < -1000:
            inc2 -= 2000
        if 300-inc2 > 0:
            mask_signal = signal.square((np.pi*x+inc + 0 )*0.5)*s_amp + s_amp
            mask_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc +np.pi)*0.5)*s_amp + s_amp
        else:
            mask_signal = signal.square((np.pi*x+inc + np.pi )*0.5)*s_amp + s_amp
            mask_signal[300-inc2:] = signal.square((np.pi*x[300-inc2:]+inc + 0)*0.5)*s_amp + s_amp
        y_carry = np.sin((np.pi*x+inc + np.pi*(mask_signal/(2*s_amp)))*(c_frq/2))*c_amp
        if y_signal[0] == 0:
            pass
        return y_signal, y_carry



def normalize(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(-100, 100)
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
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

y_signal = np.sin((x))
y_max = max(y_signal)
y_carry = np.sin((x)*c_frq)*c_amp
s_line, = s_ax.plot(x, y_signal, 'k')
c_line, = c_ax.plot(x, y_carry)

y_signal = discr_signal_gen(0)

sm_line, = m_ax.plot(x, y_signal, 'k')
cm_line, = m_ax.plot(x, y_carry, 'r')
spm_line, = m_ax.plot(x, y_signal, 'k')

bit_0 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_1 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_2 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_3 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_4 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_5 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_6 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_7 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_8 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)
bit_9 = s_ax.text(0, 0.6, '', transform = s_ax.transAxes, fontsize = 18)

s_ax.cla()
c_ax.cla()
m_ax.cla()

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)

s_ax.legend([s_line], ['Сигнал'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line, sm_line], ['Модулированное несущее колебание', 'Сигнал'], loc = 'upper center', frameon=False, ncol=2)



ani1 = animation.FuncAnimation(fig, s_ani, np.arange(1, 1258), interval=20, blit=True)
ani2 = animation.FuncAnimation(fig, c_ani, np.arange(1, 127), interval=20, blit=True) #if speed = 10.0 => range = 125, interval =20
ani3 = animation.FuncAnimation(fig, m_ani, np.arange(1, 1258), interval=20, blit=True)

'''import inspect

print(inspect.getmembers(bit_0, predicate=inspect.ismethod))'''

root.mainloop()