from tkinter import *
from tkinter import ttk
import time, sys, math

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
plot_container.grid(row = 0, column = 0,columnspan = 2, rowspan = 20, sticky = ('N, W, E, S'), padx = 3, pady = 6)
plot_container.configure(background = background_, foreground = foreground_)


width = 1200
height = 300
center = height // 2
x_increment = 1
x_factor = 0.1 # width stretch
y_amplitude = 80 # height stretch
x = [i for i in range(10, width)]
#first frame with signal plot
signal_frame = Canvas(plot_container, width = width, height = height, background= background_)
signal_frame.grid(row = 0, column = 0, padx = 20, pady = 20)
#line description
signal_frame.create_text(30, 30, anchor=SW, text='signal plot', font = font_, fill = foreground_)
signal_frame.create_line(140, 18, 200, 18, width = 5, fill = 'red')
center_line = signal_frame.create_line(10, center, width, center, fill=foreground_, arrow = LAST, width = 3)
vertical_line_up = signal_frame.create_line(10, center, 10 , 5, fill=foreground_, arrow = LAST, width = 3)
vertical_line_down = signal_frame.create_line(10, center, 10 , height - 5, fill=foreground_, arrow = LAST, width = 3)


def anim():
        #plot generation and drawing
        frame = 0
        while True:
            try:
                y = [int(math.sin((i+frame) * x_factor) * y_amplitude) + center for i in x]
                xy = list(zip(x, y))
                sin_line = signal_frame.create_line(xy, fill = 'red', width = 1)
                if frame < 125:
                
                   frame += 1
                else:
                    frame = 0
                signal_frame.update()
                time.sleep(.01)
                signal_frame.delete(sin_line)
            except Exception:
                sys.exit(0)
        root.mainloop()


freq_lbl = ttk.Label(modulation, text = 'Частота', font = font_)
freq_lbl.grid(row = 0, column = 2, sticky = ('E'), padx = (20, 5))
freq_lbl.configure(background = background_, foreground = foreground_)

frequency = IntVar()
freq_box = Spinbox(modulation, from_ = 1, to = 100, textvariable = frequency, font = font_, foreground = foreground_)
freq_box.grid(row = 0, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 21)

amp_lbl = ttk.Label(modulation, text = 'Amplitude', font = font_)
amp_lbl.grid(row = 1, column = 2, sticky = ('W'), padx = (20, 5))
amp_lbl.configure(background = background_, foreground = foreground_)

amplitude = IntVar()
ampl_box = Spinbox(modulation, from_ = 1, to = 300, textvariable = amplitude, font = font_)
ampl_box.grid(row = 1, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 2)

type_m_lbl = ttk.Label(modulation, text = 'Type', font = font_)
type_m_lbl.grid(row = 2, column = 2, sticky = 'E', padx = (20, 5))
type_m_lbl.configure(background = background_, foreground = foreground_)

type_m = StringVar()
type_modulation = ttk.Combobox(modulation, state = 'readonly', textvariable = type_m , font = font_)
type_modulation.grid(row = 2, column = 3, sticky = ('N, W, E, S'), padx = 2, pady = 20)
type_modulation['values'] = ('Амплитудная', 'Частотная', 'Фазовая')
type_modulation.current(0)
root.option_add('*TCombobox*Listbox.font', font_)

'''
#plot generation and drawing
frame = 0
while True:
    try:
        y = [int(math.sin((i+frame) * x_factor) * y_amplitude) + center for i in x]
        xy = list(zip(x, y))
        sin_line = signal_frame.create_line(xy, fill = 'red', width = 1)
        if frame < 125:
 
           frame += 1
        else:
            frame = 0
        signal_frame.update()
        time.sleep(.01)
        signal_frame.delete(sin_line)
    except Exception:
        sys.exit(0)
'''
anim()
#root.mainloop()