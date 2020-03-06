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
import random

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

bits_tut = False
if not bits_tut:
  bits = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
  bits_tut = True

fig = plt.Figure(figsize=(12, 10))

new_bits = []
for i in range(0, 10):
  new_bits += [bits[i]*50]*100

def update_plot():
  c_frq = int(carry_freq.get())
  fig.canvas.draw_idle()
  new_bits = []
  for i in range(0, 10):
    new_bits += [bits[i]*50]*100

  s_ax.cla()
  c_ax.cla()
  m_ax.cla()

  y_signal = np.array(new_bits)
  y_carry = np.sin((np.pi*x)*c_frq/2)*c_amp
  s_line, = s_ax.plot(x, y_signal, 'k')
  c_line, = c_ax.plot(x, y_carry)


  y_carry = get_carry(x, y_signal)
  cm_line, = m_ax.plot(x, y_carry, 'r')
  sm_line, = m_ax.plot(x, y_signal, 'k')


  s_ax.text(0.04, 0.6, bits[0], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.14, 0.6, bits[1], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.24, 0.6, bits[2], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.34, 0.6, bits[3], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.44, 0.6, bits[4], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.54, 0.6, bits[5], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.64, 0.6, bits[6], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.74, 0.6, bits[7], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.84, 0.6, bits[8], transform = s_ax.transAxes, fontsize = 18)
  s_ax.text(0.94, 0.6, bits[9], transform = s_ax.transAxes, fontsize = 18)

  normalize(s_ax)
  normalize(c_ax)
  normalize(m_ax)

  s_ax.legend([s_line], ['Сигнал'], loc = 'upper center', frameon=False)
  c_ax.legend([c_line], ['Несущее колебание'], loc = 'upper center', frameon=False)
  m_ax.legend([cm_line, sm_line], ['Модулированный сигнал', 'Сигнал'], loc = 'upper center', frameon=False, ncol=2)

def carry_freq_change(event=None):
  update_plot()

def type_changed(event=None):
  update_plot()

def pass_func():
  return 0

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

def oz_change(num):
  if num == 0:
    return 1
  else:
    return 0

def get_carry(x, y_signal):
  c_frq = int(carry_freq.get())

  if type_manipulation.get() == 'ОФМт':
    mask = []
    cur_bit = 0
    for i in range(0, 10):
      if bits[i] == 1:
        mask.append(oz_change(cur_bit))
        cur_bit = oz_change(cur_bit)
      else:
        mask.append(cur_bit)

    y_signal = []
    for i in range(0, 10):
      y_signal += [mask[i]*50]*100
    y_signal = np.array(y_signal)

  config = {
  'АМт': "np.sin((np.pi*x)*c_frq/2)*c_amp*(y_signal/(2*s_amp))",
  'ЧМт': "np.sin((np.pi*x)*(c_frq/2+8*(y_signal/(2*s_amp))))*c_amp",#"np.sin((x)*(c_frq+c_frq*(y_signal/(2*s_amp))))*c_amp",
  'ФМт': "np.sin((np.pi*x + np.pi*(y_signal/(2*s_amp)))*(c_frq/2))*c_amp",
  'ОФМт': "np.sin((np.pi*x + np.pi*(y_signal/(2*s_amp)))*(c_frq/2))*c_amp"
  }

  return eval(config[type_manipulation.get()])

def button_bit_click_0(event=None):
  bits.pop(0)
  bits.append(0)
  update_plot()

def button_bit_click_1(event=None):
  bits.pop(0)
  bits.append(1)
  update_plot()

def keyboard_event(event):
  key = event.char
  if int(key) in [0,1]:
    bits.pop(0)
    bits.append(int(key))

    update_plot()

plot_container = tk.LabelFrame(root, text = '', height = 960, width = 1280, font = font_)
plot_container.grid(row = 0, column = 0, rowspan = 9, padx = 5, pady = 5)
plot_container.configure(background = background_, foreground = foreground_)

#main label
type_text = tk.StringVar()
type_text.set('Амплитудная манипуляция')
type_label = ttk.Label(plot_container, textvariable = type_text, font = font_, background = background_)
type_label.grid(row = 0, column = 0, sticky = ('N'), padx = 2, pady = 5)


#Carrying frequency
carry_freq_lbl = ttk.Label(root, text = 'Частота', font = font_)
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
carry_amp_box = tk.Spinbox(root, from_ = 5, to = 300, textvariable = carry_amp, font = font_, foreground = foreground_, command = pass_func, increment = 5.0, state = 'disable')
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
type_manipulation.bind('<<ComboboxSelected>>', type_changed)

button_0 = tk.Button(root, text = '   0   ', command = button_bit_click_0, font = font_, bg = 'white', width = 4)
button_0.grid(row = 2, column = 1, sticky = ('E', 'S'), padx = (40, 5), pady = 5)

button_1 = tk.Button(root, text = '   1   ', command = button_bit_click_1, font = font_, bg = 'white', width = 4)
button_1.grid(row = 2, column = 2, sticky = ('E', 'S'), padx = (5, 40), pady = 5)

#variables
s_amp = None

# def init_plot():
s_amp = 25

c_frq = int(carry_freq.get())
c_amp = int(carry_amp.get())

#plotting
fig = plt.Figure(figsize=(12, 10))
x = np.arange(0, 10, 0.01)

canvas = FigureCanvasTkAgg(fig, master=plot_container)
canvas.get_tk_widget().grid(row=1,column=0)

s_ax = fig.add_subplot(311)
c_ax = fig.add_subplot(312)
m_ax = fig.add_subplot(313)

y_signal = np.array(new_bits)
y_max = max(y_signal)
y_carry = np.sin((np.pi*x)*c_frq/2)*c_amp

s_line, = s_ax.plot(x, y_signal, 'k')
c_line, = c_ax.plot(x, y_carry)

y_carry = np.sin((np.pi*x)*c_frq/2)*c_amp*(y_signal/(2*s_amp))

cm_line, = m_ax.plot(x, y_carry, 'r')
sm_line, = m_ax.plot(x, y_signal, 'k')

s_ax.text(0.04, 0.6, bits[0], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.14, 0.6, bits[1], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.24, 0.6, bits[2], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.34, 0.6, bits[3], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.44, 0.6, bits[4], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.54, 0.6, bits[5], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.64, 0.6, bits[6], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.74, 0.6, bits[7], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.84, 0.6, bits[8], transform = s_ax.transAxes, fontsize = 18)
s_ax.text(0.94, 0.6, bits[9], transform = s_ax.transAxes, fontsize = 18)

normalize(s_ax)
normalize(c_ax)
normalize(m_ax)
s_ax.legend([s_line], ['Сигнал'], loc = 'upper center', frameon=False)
c_ax.legend([c_line], ['Несущее колебание'], loc = 'upper center', frameon=False)
m_ax.legend([cm_line, sm_line], ['Модулированный сигнал', 'Сигнал'], loc = 'upper center', frameon=False, ncol=2)

root.bind("<Key>", keyboard_event)

root.mainloop()