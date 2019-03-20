from tkinter import *
from tkinter import ttk
import time, sys, math

#TODO:
#   !!!)repare animation +
#   1)thinking about amp and freq values and describe them +-
#   2)create events for changing amp and freq +
#   3)add phase constant signal_phi +
#   4)add units labels like kGhz and others (i think it's not necessary)
#   5)add units for scales +
#   6)bind entry button+
#   7)add carrying oscillation +
#   8) freeze animation button === signal/carrying _frames = 0 as a constant
#   9)sinchronize carry_amplitude with signal_amplitude +
#   10)add amplitude modulation +
#   11)add combobox events and reconfigure constants architecture
#   12)add freq modulation

font_ = ('Arial', '14')
background_ = '#f5f5f5'
foreground_ = '#2c2f33'

root = Tk()
root.configure(background = background_)
root.title('modulation')
root.geometry('1920x1080')
root.resizable(1920, 1080)


style = ttk.Style()
style.theme_create( "hyummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] ,
                                    'background': background_} },
        "TNotebook.Tab": {"configure": {"padding": [5, 1], 
                                        "background": 'white', 
                                        'font' : font_},
            "map":       {"background": [("selected", background_)],
                          "expand": [("selected", [1, 1, 1, 0])],
                          'foreground': [('selected', foreground_)]} } ,
        'TCombobox':{'configure':{'selectbackground': 'white',
                                       'fieldbackground': 'white',
                                       #'background': 'gray',
                                       'selectforeground': foreground_,
                                       #'font': font_
                                       }}} )

style.theme_use("hyummy")

note = ttk.Notebook(root)
note.configure(width = 1920, height = 1080)

modulation = Frame(note)
modulation.configure(background = background_)
manipulation = ttk.Frame(note)
note.add(modulation, text = 'modulation')
note.add(manipulation, text = 'manipulation')
note.grid(row = 0, column = 0, sticky = ('N, W'))


plot_container = LabelFrame(modulation,text = 'here would be some graphics', height = 960, width = 1280, font = font_)
plot_container.grid(row = 0, column = 0,columnspan = 2, rowspan = 60, sticky = ('N, W, E, S'), padx = 3, pady = 6)
plot_container.configure(background = background_, foreground = foreground_)

#canvas frames creating
#TODO: add diffrent constant for signal, carrying oscillation and modulation plots
width = 1200
height = 300
center = height // 2
#x_increment = 1
#signal
signal_x_factor = 0.02 # width stretch
signal_y_amplitude = 35 # height stretch
signal_phi = 0
#carrying osci
carry_x_factor = 0.4 # width stretch
carry_y_amplitude = 35 # height stretch
carry_phi = 0
#modulation
#modulation_x_factor = 0.1 # width stretch
#modulation_y_amplitude = 80 # height stretch
#modulation_phi = 0

x = [i for i in range(10, width)]

#first frame with signal plot
signal_frame = Canvas(plot_container, width = width, height = height, background= background_)
signal_frame.grid(row = 0, column = 0, padx = 20, pady = 10)
#line description
signal_frame.create_text(80, 30, anchor=SW, text='signal plot', font = font_, fill = foreground_)
signal_frame.create_line(190, 18, 240, 18, width = 5, fill = 'red')
signal_frame.create_text(20, 30, anchor = SW, text = 'U(t)', font = font_, fill = foreground_)
signal_frame.create_text(width-10, center+20, anchor = E, text = 't', font = font_, fill = foreground_)
center_line = signal_frame.create_line(10, center, width, center, fill=foreground_, arrow = LAST, width = 3)
vertical_line_up = signal_frame.create_line(10, center, 10 , 5, fill=foreground_, arrow = LAST, width = 3)
vertical_line_down = signal_frame.create_line(10, center, 10 , height - 5, fill=foreground_, arrow = LAST, width = 3)

#second frame with carrying oscillation
carry_frame = Canvas(plot_container, width = width, height = height, background= background_)
carry_frame.grid(row = 21, column = 0, padx = 20, pady = 10)
#line description
carry_frame.create_text(80, 30, anchor=SW, text='несущее колебание', font = font_, fill = foreground_)
carry_frame.create_line(290, 18, 340, 18, width = 5, fill = 'blue')
carry_frame.create_text(20, 30, anchor = SW, text = 'U(t)', font = font_, fill = foreground_)
carry_frame.create_text(width-10, center+20, anchor = E, text = 't', font = font_, fill = foreground_)
center_line = carry_frame.create_line(10, center, width, center, fill=foreground_, arrow = LAST, width = 3)
vertical_line_up = carry_frame.create_line(10, center, 10 , 5, fill=foreground_, arrow = LAST, width = 3)
vertical_line_down = carry_frame.create_line(10, center, 10 , height - 5, fill=foreground_, arrow = LAST, width = 3)

#third frame with carrying oscillation
mod_frame = Canvas(plot_container, width = width, height = height, background= background_)
mod_frame.grid(row = 41, column = 0, padx = 20, pady = 10)
#line description
mod_frame.create_text(80, 30, anchor=SW, text='промодулированное несущее колебание', font = font_, fill = foreground_)
mod_frame.create_line(500, 18, 550, 18, width = 5, fill = 'blue')
mod_frame.create_text(570, 30, anchor=SW, text='форма сигнала', font = font_, fill = foreground_)
mod_frame.create_line(730, 18, 770, 18, width = 5, fill = 'red')
mod_frame.create_text(20, 30, anchor = SW, text = 'U(t)', font = font_, fill = foreground_)
mod_frame.create_text(width-10, center+20, anchor = E, text = 't', font = font_, fill = foreground_)
center_line = mod_frame.create_line(10, center, width, center, fill=foreground_, arrow = LAST, width = 3)
vertical_line_up = mod_frame.create_line(10, center, 10 , 5, fill=foreground_, arrow = LAST, width = 3)
vertical_line_down = mod_frame.create_line(10, center, 10 , height - 5, fill=foreground_, arrow = LAST, width = 3)


def signal_freq_change(event=None):
    global signal_x_factor
    signal_x_factor = int(signal_frequency.get()) / 100

def carry_freq_change(event=None):
    global carry_x_factor
    carry_x_factor = int(carry_frequency.get()) / 100

def signal_amp_change(event=None):
    global signal_y_amplitude
    signal_y_amplitude = int(signal_amplitude.get())

def carry_amp_change(event=None):
    global carry_y_amplitude
    carry_y_amplitude = int(carry_amplitude.get())

def signal_phase_change(event=None):
    global signal_phi
    signal_phi = int(signal_phase.get())

def carry_phase_change(event=None):
    global carry_phi
    carry_phi = int(carry_phase.get())

def anim():
    #plot generation and drawing
    signal_frames = 0
    carry_frames = 0
    mod_frames = 0
    global signal_y_amplitude, carry_y_amplitude, x
    while True:
        try:
            signal_y = [int(math.sin((i+signal_frames + signal_phi) * signal_x_factor) * signal_y_amplitude) + center for i in x]
            signal_xy = list(zip(x, signal_y))
            amp_coef = max(signal_y) - center

            #maybe this decision is note optimal
            '''if carry_y_amplitude < signal_y_amplitude:
                carry_y_amplitude = signal_y_amplitude
                carry_amplitude.set(signal_y_amplitude)
            '''
            #temporary option, in future could change it for definite func
            carry_y_amplitude = signal_y_amplitude

            carry_y = [int(math.sin((i+carry_frames + carry_phi) * carry_x_factor) * carry_y_amplitude * 2) + center for i in x]
            carry_xy = list(zip(x, carry_y))
            max_carry_amp = center - max(carry_y) 

            mod_y = [int(math.sin((j+carry_frames + carry_phi) * carry_x_factor)*((signal_y[i] - center * 1.5) / (amp_coef)) * max_carry_amp/2 + center) for i, j in enumerate(x)]
            mod_xy = list(zip(x, mod_y))
            mod_sig_y = [int(math.sin((i+signal_frames + signal_phi) * signal_x_factor) * signal_y_amplitude) + (center/2) for i in x]
            mod_sig_xy = list(zip(x, mod_sig_y))

            #print(max(carry_y)- center) === 39
            #print(min(signal_y), max(signal_y))
            #print(min(carry_y), max(carry_y))

            signal_sin_line = signal_frame.create_line(signal_xy, fill = 'red', width = 1)
            carry_sin_line = carry_frame.create_line(carry_xy, fill = 'blue', width = 1)
            mod_sin_line = mod_frame.create_line(mod_xy, fill = 'blue', width = 1)
            mod_signal_sin_line = mod_frame.create_line(mod_sig_xy, fill = 'red', width =1)

            if signal_frames < ((1/signal_x_factor) * 1250): #(signal_x_factor * 1250): or freq = 10 === 63
               signal_frames += 1
               pass
            else:
                signal_frames = 0

            if carry_frames < ((1/carry_x_factor) * 1250):
               carry_frames += 1
               pass
            else:
                carry_frames = 0

            if mod_frames < ((1/carry_x_factor) * 1250): #correct constants
               mod_frames += 1
               pass
            else:
                mod_frames = 0

            plot_container.update()
            time.sleep(.01)
            signal_frame.delete(signal_sin_line)
            carry_frame.delete(carry_sin_line)
            mod_frame.delete(mod_sin_line)
            mod_frame.delete(mod_signal_sin_line)
        except Exception as ex:
            print(type(ex).__name__, ex.args)
            sys.exit(0)
    root.mainloop()

#Signal frequency
signal_freq_lbl = ttk.Label(modulation, text = 'Частота', font = font_)
signal_freq_lbl.grid(row = 3, column = 2, sticky = ('E'), padx = (20, 5))
signal_freq_lbl.configure(background = background_, foreground = foreground_)

signal_frequency = IntVar()
signal_frequency.set(2)
signal_freq_box = Spinbox(modulation, from_ = 1, to = 100, textvariable = signal_frequency, font = font_, foreground = foreground_, command = signal_freq_change)
signal_freq_box.grid(row = 3, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 21)
signal_freq_box.bind('<Return>', signal_freq_change)


#Signal Amplitude
signal_amp_lbl = ttk.Label(modulation, text = 'Amplitude', font = font_)
signal_amp_lbl.grid(row = 4, column = 2, sticky = ('W'), padx = (20, 5))
signal_amp_lbl.configure(background = background_, foreground = foreground_)

signal_amplitude = IntVar()
signal_amplitude.set(35)
signal_ampl_box = Spinbox(modulation, from_ = 5, to = 300, textvariable = signal_amplitude, font = font_, command = signal_amp_change, increment = 5.0)
signal_ampl_box.grid(row = 4, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 2)
signal_ampl_box.bind('<Return>', signal_amp_change)


#Signal Phase
signal_phase_lbl = ttk.Label(modulation, text = 'Фаза', font = font_)
signal_phase_lbl.grid(row = 5, column = 2, sticky = ('W'), padx = (70, 5))
signal_phase_lbl.configure(background = background_, foreground = foreground_)

signal_phase = IntVar()
signal_phase.set(0)
signal_phase_box = Spinbox(modulation, from_ = 0, to = 300, textvariable = signal_phase, font = font_, command = signal_phase_change, increment = 10.0)
signal_phase_box.grid(row = 5, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 21)
signal_phase_box.bind('<Return>', signal_phase_change)


#Carrying frequency
carry_freq_lbl = ttk.Label(modulation, text = 'Частота', font = font_)
carry_freq_lbl.grid(row = 21, column = 2, sticky = ('E'), padx = (20, 5))
carry_freq_lbl.configure(background = background_, foreground = foreground_)

carry_frequency = IntVar()
carry_frequency.set(40)
carry_freq_box = Spinbox(modulation, from_ = 1, to = 100, textvariable = carry_frequency, font = font_, foreground = foreground_, command = carry_freq_change)
carry_freq_box.grid(row = 21, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 21)
carry_freq_box.bind('<Return>', carry_freq_change)


#Carry Amplitude !!!disable spinbox and changed textvariable to signal amplitude!!!
carry_amp_lbl = ttk.Label(modulation, text = 'Amplitude', font = font_)
carry_amp_lbl.grid(row = 22, column = 2, sticky = ('W'), padx = (20, 5))
carry_amp_lbl.configure(background = background_, foreground = foreground_)

carry_amplitude = IntVar()
carry_amplitude.set(40)
carry_ampl_box = Spinbox(modulation, from_ = 0, to = 300, textvariable = signal_amplitude, font = font_, command = carry_amp_change, increment = 5.0, state = 'disable')
carry_ampl_box.grid(row = 22, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 2)
carry_ampl_box.bind('<Return>', carry_amp_change)

#Carry Phase
carry_phase_lbl = ttk.Label(modulation, text = 'Фаза', font = font_)
carry_phase_lbl.grid(row = 23, column = 2, sticky = ('W'), padx = (70, 5))
carry_phase_lbl.configure(background = background_, foreground = foreground_)

carry_phase = IntVar()
carry_phase.set(0)
carry_phase_box = Spinbox(modulation, from_ = 0, to = 300, textvariable = carry_phase, font = font_, command = carry_phase_change, increment = 10.0)
carry_phase_box.grid(row = 23, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 21)
carry_phase_box.bind('<Return>', carry_phase_change)


#Type of modulation switcher
type_m_lbl = ttk.Label(modulation, text = 'Type', font = font_)
type_m_lbl.grid(row = 41, column = 2, sticky = 'E', padx = (20, 5))
type_m_lbl.configure(background = background_, foreground = foreground_)

type_m = StringVar()
type_modulation = ttk.Combobox(modulation, state = 'readonly', textvariable = type_m , font = font_)
type_modulation.grid(row = 41, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 20)
type_modulation['values'] = ('Амплитудная', 'Частотная', 'Фазовая')
type_modulation.current(0)
root.option_add('*TCombobox*Listbox.font', font_)

anim()
#root.mainloop()