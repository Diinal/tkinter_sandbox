import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
import random

freq = 1
amp = 1
carry_freq = 0.2
carry_amp = 1
x = np.arange(0, 10, 0.01)

#аналоговый сигнал
y_signal = np.sin(x*freq) *amp +1
#дискретный сигнал
y_signal = signal.square(1 *np.pi *x) + 1
y_signal[300:400] = 2
y_signal[400:] = signal.square(1 *np.pi *x[400:] +np.pi) +1
y_signal[700:800] = 0
y_signal[800:] = signal.square(1 *np.pi *x[800:]) +1
y_carry = 2*np.sin(8*np.pi*x)


fig = plt.figure()
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax.set_ylim(-3, 3)
ax.set_xlim(0, 10)
ax.spines['bottom'].set_position('center')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax2.set_ylim(-3, 3)
ax2.spines['bottom'].set_position('center')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax3.set_ylim(-3, 3)
ax3.spines['bottom'].set_position('center')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

line, = ax.plot(x, y_signal)
line1, = ax2.plot(x, y_carry)
line2, = ax3.plot(x, y_signal)
ax.xaxis.set_major_locator(plt.MaxNLocator(20))
y_carry = 2*np.sin(4*np.pi*x +np.pi*(y_signal/2))



#line3, = ax3.plot(x, y_carry*y_signal/2)
line3, = ax3.plot(x, y_carry)

plt.show()