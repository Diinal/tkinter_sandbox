import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

freq = 0.1
amp = 1
carry_freq = 0.2
carry_amp = 1
x = np.arange(0, 20, 0.01)

#аналоговый сигнал
y_signal = np.sin(x*freq) *amp 

#дискретный сигнал
'''
y_signal[:300] = 1
y_signal[300:600] = 0
y_signal[600:] = -1
'''

#y_carry = np.cos(2*np.pi*carry_freq*x + 2*np.pi*y_signal*1)*carry_amp
#y_carry = np.cos(2*np.pi*carry_freq*x + (amp*9*freq)*np.sin(2*np.pi*freq*x))*carry_amp
#y_carry = np.sin(x*carry_freq + (y_signal*0.5))*carry_amp
y_signal = 2*np.sin(2*np.pi*0.25*x)
y_carry = 2*np.sin(2*np.pi*x)
y_carry = 2*np.sin(2*np.pi*x - 2*np.cos(2*np.pi*0.25*x))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(-2, 2)
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

line, = ax.plot(x, y_signal)
line1, = ax.plot(x, y_carry)

plt.show()